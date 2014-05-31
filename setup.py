# -*- coding: utf-8 -*_

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import sys

import dotfav


long_desc = '''
'''


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


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
    install_requires=['pathlib'],
    tests_require=['pytest'],
    cmdclass = { 'test': PyTest },
)
