from django.db import models

from tsearch2.models import SearchableModel, SearchManager


class Book(SearchableModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    preface = models.TextField(blank=True)

    objects = SearchManager({
        'title': 'A', 'author': 'A', 'preface': 'D',
    })

    def __unicode__(self):
        return self.title


class ISBNBook(SearchableModel):
    # test custom primary key fields
    isbn = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    preface = models.TextField(blank=True)

    objects = SearchManager({
        'title': 'A', 'author': 'A', 'preface': 'D',
    })

    def __unicode__(self):
        return self.title
