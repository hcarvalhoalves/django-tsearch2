from django.db import models
from django.contrib.gis.db import models as gis_models

from tsearch2.models import SearchableModel, SearchManager
from tsearch2.gis import SearchGeoManager


class Location(SearchableModel):
    name = models.CharField(max_length=255)
    latlon = gis_models.PointField()

    objects = SearchGeoManager({
        'name': 'A',
    })

    def __unicode__(self):
        return self.name
