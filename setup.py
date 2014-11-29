from setuptools import setup

setup(
    name = "django-tsearch2",
    version = "0.4.1",
    url = "http://github.com/hcarvalhoalves/django-tsearch2",
    description = "Postgresql's full text search support for Django",
    author = "Henrique Carvalho Alves",
    author_email = "hcarvalhoalves@gmail.com",
    packages = [
        'tsearch2',
        'tsearch2.management',
        'tsearch2.management.commands'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe = False,
)
