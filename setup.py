#!/usr/bin/env python3
# coding: utf-8
"""VMware Aria Operations for Applications Pyformance Library.

The Operations for Applications Pyformance library provides
Wavefront reporters (via proxy and direct ingestion) and a
simple abstraction for tagging at the host level.
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
    version='1.2.3',
    author='VMware Aria Operations for Applications Team',
    author_email='chitimba@wavefront.com',
    url='https://github.com/wavefrontHQ/wavefront-pyformance',
    license='Apache-2.0',
    description='VMware Aria Operations for Applications Pyformance Library',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords=[
        'Distributed Tracing',
        'Logging',
        'Metrics',
        'Monitoring',
        'Observability',
        'PyFormance',
        'Tracing',
        'Wavefront',
        'Wavefront Pyformance'
        ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring'
        ],
    include_package_data=True,
    packages=setuptools.find_packages(exclude=('tests',)),
    install_requires=(
        'pyformance>=0.4',
        'wavefront-sdk-python>=1.8.0',
        'psutil>=5.6.3'
        )
)
