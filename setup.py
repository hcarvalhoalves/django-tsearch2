from setuptools import setup
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass


setup(
    name = "django-tsearch2",
    version = "0.2",
    packages = ['tsearch2', 'tsearch2.management', 'tsearch2.management.commands'],
    author = "Henrique Carvalho Alves",
    author_email = "hcarvalhoalves@gmail.com",
    description = "TSearch2 support for Django",
    url = "http://github.com/hcarvalhoalves/django-tsearch2",
)