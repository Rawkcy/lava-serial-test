#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='lava-serial-test',
    version=':versiontools:lava_serial_test:',
    author='Roxanne Guo',
    author_email='roxanne@gumstix.com',
    description='Gumstix boards test execution framework over serial interface',
    long_description=open("README").read(),
    entry_points="""
    [console_scripts]
    lava-serial-test=lava_serial_test.main:__main__
    """,
    classifiers=[
        "Development Status :: Pre - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Testing",
    ],
    install_requires=[
        'lava-tool >= 0.2',
        'versiontools >= 1.4',
        'pexpect >= 2.4',
    ],
    setup_requires=[
        'versiontools >= 1.4'
    ],
    zip_safe=False,
    include_packages_data=True)
