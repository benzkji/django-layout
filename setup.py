#!/usr/bin/env python
from setuptools import setup, find_packages

# probably not gonna install anyway, as I want my media files under control
# and not gone when re-initialising the env.
setup(
    name='{{ project_name }}',
    version='1.0',
    description="",
    author="bnzk",
    author_email='bnzk@bnzk.ch',
    url='',
    packages=find_packages(),
    package_data={'{{ project_name }}': ['static/*.*', 'templates/*.*']},
    scripts=['manage.py'],
)
