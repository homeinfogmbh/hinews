#! /usr/bin/env python3
"""Installation script."""

from setuptools import setup


setup(
    name='hinews',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    install_requires=[
        'configlib',
        'dscms3',
        'filedb',
        'flask',
        'his',
        'mdb',
        'peewee',
        'peeweeplus',
        'pil',
        'wsgilib'
    ],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info@homeinfo.de>',
    maintainer='Richard Neumann',
    maintainer_email='<r.neumann@homeinfo.de>',
    packages=['hinews', 'hinews.messages', 'hinews.wsgi'],
    description='HOMEINFO news API.'
)
