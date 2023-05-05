#!/usr/bin/env python3
from setuptools import find_packages, setup
setup(
    name='grouppy',
    packages=find_packages(),
    version='0.1.1',
    description='A Python Library for interacting with the GroupMe Rest API ',
    author='TheKrafter',
    license='GPL-3.0',
    install_requires=['requests', 'flask', 'guli', 'websockets'],
    setup_requires=['setuptools', 'pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)