#!/usr/bin/env python3
# coding: utf-8
"""Wavefront Pyformance Library.

The Wavefront Pyformance library provides Wavefront reporters
(via proxy and direct ingestion) and a simple abstraction for
tagging at the host level.
It also includes support for Wavefront delta counters.
"""

import os
try:
    import setuptools
except ImportError:
    import sys
    sys.exit('Failed to import setuptools. Do pip install setuptools first.')

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'README.md')) as fd:
    LONG_DESCRIPTION = fd.read()

setuptools.setup(
    name='wavefront-pyformance',
    version='1.0.0',
    author='Wavefront by VMware',
    author_email='chitimba@wavefront.com',
    url='https://github.com/wavefrontHQ/wavefront-pyformance',
    license='Apache-2.0',
    description='Wavefront Pyformance Library',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords=[
        'PyFormance',
        'Wavefront',
        'Wavefront Pyformance'
        ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        ],
    include_package_data=True,
    packages=setuptools.find_packages(exclude=('tests',)),
    install_requires=(
        'pyformance>=0.4',
        'wavefront-sdk-python>=1.1'
        )
)
