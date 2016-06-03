#!/usr/bin/env python

from setuptools import setup

VERSION = "0.0.1"
DESCRIPTION = "Tools based on the Million Songs DB: http://labrosa.ee.columbia.edu/millionsong/"

setup(
    name='mm-songs-db-tools',
    version=VERSION,
    description=DESCRIPTION,
    author="Sam Sandberg",
    url='https://github.com/rcrdclub/mm-songs-db-tools',
    license='GNU GPL v3.0',
    packages=["mmsongsdbtools"],
    # TODO: Write longer description
    long_description=DESCRIPTION,
    install_requires=[
        'pytables',
    ],
)
