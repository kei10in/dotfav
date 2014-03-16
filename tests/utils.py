# -*- coding: utf-8 -*_

import os
import shutil
import json

import dotfav


class Path(str):
    def remove(self):
        if self.isdir():
            shutil.rmtree(test_temp)
        elif self.isfile():
            shutil.unlink(test_temp)

    def mkdir(self):
        os.mkdir(self)

    def children(self):
        return (self.__class__(os.path.join(self, x)) for x in os.listdir(self))

    def isdir(self):
        return os.path.isdir(self)

    def isfile(self):
        return os.path.isfile(self)

    def islink(self):
        return os.path.islink(self)

    def realpath(self):
        return self.__class__(os.path.realpath(self))

    def join(self, *args):
        return self.__class__(os.path.join(self, *args))


test_temp = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp')))
test_home = Path(os.path.join(test_temp, 'home'))
test_dotfiles = Path(os.path.join(test_temp, 'dotfiles'))
test_dotfiles_home = Path(os.path.join(test_dotfiles, 'home'))
test_dotfiles_config = test_dotfiles.join('dotfav.config')


def create_test_temp_directories():
    test_temp.mkdir()
    test_home.mkdir()
    test_dotfiles.mkdir()
    test_dotfiles_home.mkdir()


def create_file_into_dotfiles_home(filename):
    filepath = test_dotfiles_home.join(filename)
    f = open(filepath, 'w')
    f.close()


def create_directory_into_dotfiles_home(dirpath):
    dirpath = test_dotfiles_home.join(dirpath)
    os.mkdir(dirpath)


def create_config_file(config):
    with open(test_dotfiles_config, mode='w') as f:
        json.dump(config, f)


def run_dotfav(command, dotfiles, home, platform=None):
    args = ['dotfav', command, '--dotfiles', dotfiles, '--home', home]
    if platform is not None:
        args.extend(['--platform', platform])
    dotfav.main(args)
