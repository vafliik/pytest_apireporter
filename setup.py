#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-apireport',
    version='0.1.0',
    author='Pavel Pribyl',
    author_email='pribyl.pavel@gmail.com',
    maintainer='Pavel Pribyl',
    maintainer_email='pribyl.pavel@gmail.com',
    license='GNU GPL v3.0',
    url='https://github.com/vafliik/pytest-apireport',
    description='Plugin for reporting to remote APIs',
    long_description=read('README.rst'),
    py_modules=['pytest_apireport'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        'pytest11': [
            'apireport = pytest_apireport',
        ],
    },
)
