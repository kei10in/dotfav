# -*- coding: utf-8 -*_

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
import os
import re

import dotfav


long_desc = '''
'''

setup(
    name="dotfav",
    version=dotfav.__version__,
    description='dotfiles manager',
    long_description=long_desc,
    url='http://github.com/kei10in/dotfav',
    author='kei10in',
    author_email='',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
    ],
    platforms='any',
    packages=find_packages(exclude=["tests*"]),
    entry_points={
        'console_scripts': [
            'dotfav=dotfav:main',
        ],
    },
)
