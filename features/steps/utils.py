# -*- coding: utf-8 -*_

import json
from pathlib import Path

import dotfav


test_temp = Path(__file__).parent / 'temp'
home = test_temp / 'home'
dotfiles = test_temp / 'dotfiles'
dotfiles_home = dotfiles / 'home'
dotfiles_config = dotfiles / 'dotfav.config'


def create_test_temp_directories():
    test_temp.mkdir()
    home.mkdir()
    dotfiles.mkdir()
    dotfiles_home.mkdir()


def create_file_into_dotfiles_home(filename):
    filepath = dotfiles_home / filename
    f = filepath.open(mode='w')
    f.close()


def create_directory_into_dotfiles_home(dirpath):
    dirpath = dotfiles_home / dirpath
    dirpath.mkdir()


def create_config_file(config):
    config = json.loads(config)
    with dotfiles_config.open(mode='w') as f:
        json.dump(config, f)


def run_dotfav(command, dotfiles, home, platform=None):
    args = ['dotfav', command, '--dotfiles', dotfiles, '--home', home]
    if platform is not None:
        args.extend(['--platform', platform])
    dotfav.main(args)
