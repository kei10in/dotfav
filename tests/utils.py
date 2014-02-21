# -*- coding: utf-8 -*_

import os
import shutil


test_temp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp'))
test_home = os.path.join(test_temp, 'home')
test_dotfiles = os.path.join(test_temp, 'dotfiles')
test_dotfiles_home = os.path.join(test_dotfiles, 'home')


def remove_temp():
    if os.path.isdir(test_temp):
        shutil.rmtree(test_temp)
    elif os.path.isfile(test_temp):
        shutil.unlink(test_temp)


def create_test_temp_directories():
    os.mkdir(test_temp)
    os.mkdir(test_home)
    os.mkdir(test_dotfiles)
    os.mkdir(test_dotfiles_home)


def create_file_into_dotfiles_home(filename):
    filepath = os.path.join(test_dotfiles_home, filename)
    f = open(filepath, 'w')
    f.close()
