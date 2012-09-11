#!/usr/bin/env python

# from ez_setup import use_setuptools
# use_setuptools()

import os
# from setuptools import setup, Extension
from distutils.core import setup, Extension

read = lambda f: open(os.path.join(os.path.dirname(__file__), f)).read()

setup(
    name             = "poemy",
    version          = "0.1",
    description      = "Poetry Generator",
    long_description = read("README.md"),
    author           = 'Justine Tunney',
    author_email     = 'jtunney@lobstertech.com',
    license          = 'GNU AGPL v3 or later',
    install_requires = ["pycontracts"],
    py_modules       = ["poemy"],
    ext_modules      = [
        Extension("sparsehash", ["sparsehash.cpp", "MurmurHash3.cpp"]),
    ],
)
