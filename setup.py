#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

__version__ = "0.6.0"


setup(
    version=__version__,
    install_requires=open("requirements.txt").readlines(),
    tests_require=open("requirements-test.txt").readlines(),
    include_package_data=True,  # needed for data from manifest
)
