#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='hinews',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo period de>',
    requires=['his'],
    packages=['hinews', 'hinews.messages', 'hinews.wsgi'],
    scripts=['files/hinewsd'],
    data_files=[
        ('/usr/lib/systemd/system', ['files/hinews.service']),
        ('/etc/his.d/locale', ['files/hinews.ini'])],
    description='HOMEINFO news API.')
