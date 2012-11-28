from django.contrib.gis.db import models as gis_models

from tsearch2 import models as t2_models


class SearchGeoQuerySet(t2_models.SearchQuerySet, gis_models.query.GeoQuerySet):
    """
    A mixin from `SearchQuerySet` and `GeoQuerySet`.
    """


class SearchGeoManager(t2_models.SearchManager, gis_models.GeoManager):
    queryset_class = SearchGeoQuerySet
