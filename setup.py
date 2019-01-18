# coding: utf-8

"""Wavefront Pyformance Library

        The Wavefront Pyformance library provides Wavefront reporters
        (via proxy and direct ingestion) and a simple abstraction for
        tagging at the host level.
        It also includes support for Wavefront delta counters.
"""


try:
    import setuptools
except ImportError:
    import sys
    sys.exit('Failed to import setuptools. Do pip install setuptools first.')

REQUIRES = ["pyformance >= 0.4", "wavefront-sdk-python"]

setuptools.setup(
    name='wavefront_pyformance',
    version='0.9.2',
    description='Wavefront Pyformance Library',
    author_email='chitimba@wavefront.com',
    url='https://github.com/wavefrontHQ/wavefront-pyformance',
    keywords=('Pyformance', 'Wavefront Pyformance', 'Wavefront'),
    install_requires=('pyformance>=0.4', 'wavefront-sdk-python>=1.0'),
    packages=setuptools.find_packages(exclude=('tests',)),
    include_package_data=True,
    long_description="""
        The Wavefront Pyformance library provides Wavefront reporters
        (via proxy and direct ingestion) and a simple abstraction for
        tagging at the host level.
        It also includes support for Wavefront delta counters.
    """
)
