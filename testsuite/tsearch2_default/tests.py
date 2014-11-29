# coding: utf-8

__test__ = {"doctest": """
>>> from django.db import connection

>>> cursor = connection.cursor()

>>> cursor.execute('CREATE EXTENSION unaccent')

>>> cursor.execute('CREATE EXTENSION tsearch2')

>>> from testsuite.tsearch2_default.models import Book, ISBNBook

>>> Book.objects.create(title=u"The Mythical Man Month", author=u"Fred Brooks", preface=u"Essays in Software Engineering")
<Book: The Mythical Man Month>

>>> Book.objects.create(title=u"Design Patterns", author=u"Erich Gamma, Richard Helm, Ralph Johnson, John M. Vlissides", preface=u"Elements of Reusable Object-Oriented Software")
<Book: Design Patterns>

>>> Book.objects.create(title=u"Pattern: (Math Counts)", author=u"Henry Arthur Pluckrose", preface=u"Mathematics is a part of a child's world.")
<Book: Pattern: (Math Counts)>

>>> Book.objects.update_index()

>>> Book.objects.search("brooks")
[<Book: The Mythical Man Month>]

>>> sorted(Book.objects.search("pattern"))
[<Book: Design Patterns>, <Book: Pattern: (Math Counts)>]

>> Book.objects.search("henry")
[<Book: Pattern: (Math Counts)>]

>>> Book.objects.search("chicken")
[]

>>> ISBNBook.objects.create(isbn="85-359-0277-5", title=u"The Mythical Man Month", author=u"Fred Brooks", preface=u"Essays in Software Engineering")
<ISBNBook: The Mythical Man Month>

>>> ISBNBook.objects.create(isbn="1-84356-028-3", title=u"Design Patterns", author=u"Erich Gamma, Richard Helm, Ralph Johnson, John M. Vlissides", preface=u"Elements of Reusable Object-Oriented Software")
<ISBNBook: Design Patterns>

>>> ISBNBook.objects.create(isbn="0-684-84328-5", title=u"Pattern: (Math Counts)", author=u"Henry Arthur Pluckrose", preface=u"Mathematics is a part of a child's world.")
<ISBNBook: Pattern: (Math Counts)>

>>> ISBNBook.objects.update_index()

>>> ISBNBook.objects.search("brooks")
[<ISBNBook: The Mythical Man Month>]

>>> sorted(ISBNBook.objects.search("pattern"))
[<ISBNBook: Pattern: (Math Counts)>, <ISBNBook: Design Patterns>]

>> ISBNBook.objects.search("henry")
[<ISBNBook: Pattern: (Math Counts)>]

>>> ISBNBook.objects.search("chicken")
[]

"""}
