# coding: utf-8

__test__ = {"doctest": """
>>> from testsuite.tsearch2_gis.models import Location
>>> from django.contrib.gis.geos import Point

>>> Location.objects.create(name=u"Mario's Pizza", latlon=Point(12.4604, 43.9420))
<Location: Mario's Pizza>

>>> Location.objects.update_index()

>>> Location.objects.search("mario")
[<Location: Mario's Pizza>]

>>> Location.objects.search("luigi")
[]

"""}
