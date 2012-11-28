# coding: utf-8
"""
Support for full-text searchable Django models using tsearch2 in PostgreSQL.

Documentation for the tsearch2 module is available at:
http://www.postgresql.org/docs/8.3/static/textsearch-features.html

Based on Django Snippet #1328 by 'dcwatson':
http://djangosnippets.org/snippets/1328/
"""

from django.db import models
from django.db import connection
from django.db.models.signals import post_syncdb
from fields import VectorField
import os


def quote_name(s):
    from django.db import connection
    return connection.ops.quote_name(s)


class SearchQuerySet(models.query.QuerySet):

    def search(self, query, order_by_rank=True, rank_field='ts_rank'):
        """
        Returns a queryset after having applied the full-text search query. If rank_field
        is specified, it is the name of the field that will be put on each returned instance.
        When specifying a rank_field, the results will automatically be ordered by -rank_field.

        For documenation on tsquery() and ts_rank() functions, refer to:
        http://www.postgresql.org/docs/8.3/static/textsearch-controls.html
        """

        search_manager = self.model.get_search_manager()
        vector_field = quote_name(search_manager.vector_field.column)
        tsquery = u"""
        plainto_tsquery(%s, norm_text_utf8(%s))
        """

        select, select_params, order = {}, [], []
        where = [u"%s @@ %s" % (vector_field, tsquery)]
        params = [search_manager.config, query]

        if order_by_rank:
            select = {rank_field: "ts_rank(%s, %s)" % (vector_field, tsquery)}
            select_params = [search_manager.config, query]
            order = ['-%s' % rank_field]

        return self.extra(select=select, select_params=select_params,
                          where=where, params=params, order_by=order)


class SearchManager(models.Manager):
    queryset_class = SearchQuerySet
    default_indexed_fields = None
    default_config = 'pg_catalog.english'

    def __init__(self, fields=None, config=None):
        self.fields = fields and fields or self.default_indexed_fields
        self.default_weight = 'A'
        self.config = config and config or self.default_config
        self._vector_field_cache = None
        super(SearchManager, self).__init__()

    def get_query_set(self):
        return self.queryset_class(self.model)

    def contribute_to_class(self, cls, name):
        # Instances need to get to us to update their indexes.
        setattr(cls, '_search_manager', self)
        super(SearchManager, self).contribute_to_class(cls, name)

    def _find_text_fields(self):
        """
        Return the names of all CharField and TextField fields defined for this manager's model.
        """

        fields = [f for f in self.model._meta.fields if isinstance(f, (models.CharField,models.TextField))]
        return [f.name for f in fields]

    def _vector_field(self):
        """
        Returns the VectorField defined for this manager's model. There must be exactly one VectorField defined.
        """

        if self._vector_field_cache is not None:
            return self._vector_field_cache
        vectors = [f for f in self.model._meta.fields if isinstance(f, VectorField)]
        if len(vectors) != 1:
            raise ValueError(u"There must be exactly 1 VectorField defined for the %s model." % self.model._meta.object_name)
        self._vector_field_cache = vectors[0]
        return self._vector_field_cache
    vector_field = property(_vector_field)

    def _get_tsvector_sql(self, field_name, weight=None):
        sql_template = u"""
        setweight(to_tsvector('%s', coalesce(norm_text_utf8(%s), '')), '%s')
        """

        field, model, direct, m2m = self.model._meta.get_field_by_name(field_name)
        weight = weight if weight else self.default_weight

        # Local field
        if model is None:
            model = self.model
            table_name = self.model._meta.db_table
            column_name = quote_name(field.column)

        # Field is defined on some parent class, so use table name
        else:
            table_name = model._meta.db_table
            column_name = u"%s.%s" % (quote_name(table_name), quote_name(field.column))

        return (model, sql_template % (self.config, column_name, weight))

    def _get_tsvector_sql_for_fields(self, fields):
        models = {}
        fields_for_model = []

        # Dict with {'field_name': 'weight'} pairs
        if isinstance(self.fields, dict):
            for field, weight in self.fields.items():
                fields_for_model.append(self._get_tsvector_sql(field, weight))
        # Just field names
        else:
            for field in self.fields:
                fields_for_model.append(self._get_tsvector_sql(field))

        for model, tsvector_sql in fields_for_model:
            try:
                models[model] = models[model] + ' || ' + tsvector_sql
            except KeyError:
                models[model] = tsvector_sql

        return models

    def update_index(self, pk=None):
        """
        Updates the full-text index for one, many, or all instances of this manager's model.
        """

        # Iterate over fields defined to index on manager, or all text fields in model
        self.fields = self.fields if self.fields else self._find_text_fields()

        for model, tsvector_sql in self._get_tsvector_sql_for_fields(self.fields).items():

            # If one or more pks are specified, tack a WHERE clause onto the SQL.
            if pk is not None:
                if hasattr(pk, '__iter__'):
                    ids = u','.join([unicode(v) for v in pk])
                else:
                    ids = pk
                where = u"WHERE %s IN (%s)" % (
                    quote_name(model._meta.pk.column), ids
                )
            else:
                where = ''

            sql = u"UPDATE %s SET %s = %s %s;" % (
                quote_name(model._meta.db_table), quote_name(self.vector_field.column), tsvector_sql, where,
            )

        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()

    def search(self, *args, **kwargs):
        return self.get_query_set().search(*args, **kwargs)


class SearchableModel(models.Model):
    """
    A convience Model wrapper that provides an update_index method for object
    instances, as well as automatic index updating. The index is stored as a
    `tsvector` column on the model's table.
    """

    search_index = VectorField()

    class Meta:
        abstract = True

    @classmethod
    def get_search_manager(klass):
        if hasattr(klass, '_search_manager'):
            return klass._search_manager
        raise RuntimeError(u'No SearchManager for this model')

    def update_index(self):
        self.get_search_manager().update_index(pk=self.pk)

    def save(self, *args, **kwargs):
        should_update_index = kwargs.pop('update_index', True)
        super(SearchableModel, self).save(*args, **kwargs)
        if should_update_index:
            self.update_index()


SQL_NORMALIZATION_FUNCTION = u"""
drop language if exists plpythonu cascade;

create language plpythonu;

create or replace function norm_text_utf8 (string text)
  returns varchar
as $$

from unicodedata import normalize, category

return unicode(
    filter(
        lambda c: category(c) != 'Mn',
        normalize('NFKD', string.decode('utf-8'))
    )
).encode('utf-8')

$$ language plpythonu
"""

def create_normalization_function(sender, **kwargs):
    cursor = connection.cursor()
    cursor.execute(SQL_NORMALIZATION_FUNCTION)


post_syncdb.connect(create_normalization_function)
