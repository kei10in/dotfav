# -*- coding: utf-8 -*_

import json
from pathlib import Path

import dotfav


test_temp = Path(__file__).parent / 'temp'
test_home = test_temp / 'home'
test_dotfiles = test_temp / 'dotfiles'
test_dotfiles_home = test_dotfiles / 'home'
test_dotfiles_config = test_dotfiles / 'dotfav.config'


def create_test_temp_directories():
    test_temp.mkdir()
    test_home.mkdir()
    test_dotfiles.mkdir()
    test_dotfiles_home.mkdir()


def create_file_into_dotfiles_home(filename):
    filepath = test_dotfiles_home / filename
    f = filepath.open(mode='w')
    f.close()


def create_directory_into_dotfiles_home(dirpath):
    dirpath = test_dotfiles_home / dirpath
    dirpath.mkdir()


def create_config_file(config):
    with test_dotfiles_config.open(mode='w') as f:
        json.dump(config, f)


def run_dotfav(command, dotfiles, home, platform=None):
    args = ['dotfav', command, '--dotfiles', dotfiles, '--home', home]
    if platform is not None:
        args.extend(['--platform', platform])
    dotfav.main(args)
