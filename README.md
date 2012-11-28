django-tsearch2
===============
Postgresql's full text search support for Django

Installation
------------

You'll need to install the `unaccent` extension and issue:

    CREATE EXTENSION unaccent;


If you're running Postgresql 8, or don't have the `unaccent` extension
installed, you can use this plpython function:

    CREATE LANGUAGE plpythonu;

    CREATE FUNCTION unaccent (string text)
      RETURNS varchar
    AS $$

    from unicodedata import normalize, category

    return unicode(
        filter(
            lambda c: category(c) != 'Mn',
            normalize('NFKD', string.decode('utf-8'))
        )
    ).encode('utf-8')

    $$ LANGUAGE plpythonu


Usage
-----

You just need to inherit from the included `SearchableModel` class and add
a custom manager to your model classes:

    from django.db import models
    from tsearch2.models import SearchableModel, SearchManager


    class Book(SearchableModel):
        title = models.CharField(max_length=255)
        author = models.CharField(max_length=255)
        preface = models.TextField(blank=True)

        objects = SearchManager({
            'title': 'A',
            'author': 'A',
            'preface': 'D',
        })

        def __unicode__(self):
            return self.title


In this example, we're indexing the `title`, `author` and `preface` fields. The
second parameter defines the weight, from 'A' (highest) to 'D' (lowest).

Now your querysets will include a `search()` method:

    >>> Book.objects.search("pattern")
    [<Book: Pattern: (Math Counts)>, <Book: Design Patterns>]


### GeoDjango usage

Just add the `tsearch2.gis.SearchGeoManager` manager to your model instead. All
methods of this manager return a `SearchGeoQuerySet` instance that mixes both
feature sets.


Full documentation for the tsearch2 module is available at:
http://www.postgresql.org/docs/8.3/static/textsearch-features.html
