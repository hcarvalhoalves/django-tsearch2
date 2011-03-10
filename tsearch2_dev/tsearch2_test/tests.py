# coding: utf-8

__test__ = {"doctest": """
>>> from tsearch2_test.models import Book

>>> Book.objects.create(title=u"The Mythical Man Month", author=u"Fred Brooks", preface=u"Essays in Software Engineering")
<Book: The Mythical Man Month>

>>> Book.objects.create(title=u"Design Patterns", author=u"Erich Gamma, Richard Helm, Ralph Johnson, John M. Vlissides", preface=u"Elements of Reusable Object-Oriented Software")
<Book: Design Patterns>

>>> Book.objects.create(title=u"Pattern: (Math Counts)", author=u"Henry Arthur Pluckrose", preface=u"Mathematics is a part of a child's world.")
<Book: Pattern: (Math Counts)>

>>> Book.objects.update_index()

>>> Book.objects.update_index(pk=[1, 2])

>>> Book.objects.search("brooks")
[<Book: The Mythical Man Month>]

>>> Book.objects.search("pattern")
[<Book: Pattern: (Math Counts)>, <Book: Design Patterns>]

>>> Book.objects.search("chicken")
[]

>>> Book.objects.create(title=u"Testing Unicode", author=u"Renè Gonçalves", preface=u"Pretty International.")
<Book: Testing Unicode>
"""}
