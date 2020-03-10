#!/usr/bin/env python

import re
from os import path
from setuptools import setup, find_packages


requirements = [
    'aiomysql>=0.0.20',
    'SQLAlchemy>=1.3.0'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

version_file = path.join(
    path.dirname(__file__),
    'aiomysql_core',
    '__version__.py'
)
with open(version_file, 'r') as fp:
    m = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        fp.read(),
        re.M
    )
    version = m.groups(1)[0]


setup(
    name='aiomysql-core',
    version=version,
    license='MIT',
    url='https://github.com/linzhiming0826/aiomysql-core',
    author='TuoX',
    author_email='120549827@qq.com',
    description='Simple framework for aiomysql',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=requirements
)
