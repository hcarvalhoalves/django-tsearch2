from setuptools import setup

setup(
    name = "django-tsearch2",
    version = "0.2",
    packages = ['tsearch2', 'tsearch2.management', 'tsearch2.management.commands'],
    zip_safe = False,
    author = "Henrique Carvalho Alves",
    author_email = "hcarvalhoalves@gmail.com",
    description = "TSearch2 support for Django",
    url = "http://github.com/hcarvalhoalves/django-tsearch2",
)