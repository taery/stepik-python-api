#!/usr/bin/env python

from setuptools import find_packages, setup

with open('requirements.txt') as r:
    requirements = r.read().splitlines()

setup(
    name='stepik-python-api',
    packages=find_packages(),
    version='0.0.1',
    description='Python Library to work with Stepik API',
    author='Anastasia Lavrenko',
    author_email='lavrenko.a@gmail.com',
    url='https://github.com/taery/stepik-python-api',
    install_requires=requirements,
)
