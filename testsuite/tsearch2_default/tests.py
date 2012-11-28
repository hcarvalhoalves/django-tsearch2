# coding: utf-8

__test__ = {"doctest": """
>>> from testsuite.tsearch2_default.models import Book

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

"""}
