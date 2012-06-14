#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='lava-serial-test',
    version=':versiontools:lava_serial_test:',
    author='',
    author_email='',

    BLAHBLAHBLAH,

    entry_points="""
    """,
    classifiers=[],
    install_requires=[
      'lava-tool >= 0.2',
      'versiontools >= 1.4',
      'linaro_dashboard_bundle',
    ],
    setup_requires=[
      'versiontools >= 1.4'
    ],
    zip_safe=False,
    include_packages_data=True)
