from django.db import models


class VectorField(models.Field):
    """
    A field used for storing PostgreSQL's Tsearch2 search indexes.

    Documentation for the tsearch2 module is available at:
    http://www.postgresql.org/docs/8.3/static/textsearch-features.html
    """

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'null': True,
            'editable': False,
            'serialize': False,
        })
        super(VectorField, self).__init__(*args, **kwargs)

    def db_type(self, *args, **kwargs):
        return 'tsvector'


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [r"^tsearch2\.fields.\VectorField"])
except ImportError:
    pass
