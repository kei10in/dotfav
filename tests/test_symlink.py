# -*- coding: utf-8 -*-

import json

from utils import *

import dotfav


class TestScenario1(object):
    def setup_method(self, method):
        test_temp.remove()

    def test_symlink_do_nothing(self):
        self.given_there_are_dotfiles_home_directory_in_dotfiles()
        self.when_dotfiles_home_directory_contains_no_files()
        self.run_dotfav_symlink()
        self.no_files_are_symlinked()

    def test_symlink_file(self):
        self.given_there_are_dotfiles_home_directory_in_dotfiles()
        self.when_dotfiles_home_directory_contains_a_file()
        self.run_dotfav_symlink()
        self.dotfav_symlink_creates_a_symlinked_file()

    def test_symlink_directory(self):
        self.given_there_are_dotfiles_home_directory_in_dotfiles()
        self.when_dotfiles_home_directory_contains_a_directory()
        self.run_dotfav_symlink()
        self.dotfav_symlink_creates_a_symlinked_directory()

    def test_symlink_with_map_file(self):
        self.given_there_are_dotfiles_home_directory_indotfiles()
        self.when_dotfiles_contains_config_file([{
                'os': ['darwin'],
                'target': {'file': 'file.darwin'}
            }])
        self.when_dotfiles_home_contains_a_file_named('file.darwin')
        self.run_dotfav_symlink()
        self.dotfav_symlink_creates_a_symlink(
            test_dotfiles_home.join('file.darwin'),
            test_home.join('file'))

    def given_there_are_dotfiles_home_directory_in_dotfiles(self):
        create_test_temp_directories()
        assert test_dotfiles_home.isdir()

    def when_dotfiles_contains_map_file(self, config):
        with open(test_dotfiles.join('dotfav.config'), mode='w') as f:
            json.dump(config, f)

    def when_dotfiles_home_directory_contains_no_files(self):
        pass

    def when_dotfiles_home_directory_contains_a_file(self):
        self.when_dotfiles_home_directory_contains_a_file_named('file')

    def when_dotfiles_home_directory_contains_a_file_named(self, name):
        create_file_into_dotfiles_home(name)

    def when_dotfiles_home_directory_contains_a_directory(self):
        create_directory_into_dotfiles_home('directory')

    def run_dotfav_symlink(self):
        dotfav.main('dotfav symlink --home {} --dotfiles {}'.format(
            test_home, test_dotfiles).split())

    def no_files_are_symlinked(self):
        assert len([path for path in test_home.children()
                    if path.islink()
                    and path.realpath().startswith(test_dotfiles_home)]) == 0

    def dotfav_symlink_creates_a_symlinked_file(self):
        assert any(
            [path.isfile() and self.is_symlink_of_dotfiles_home(path)
             for path in test_home.children()])

    def dotfav_symlink_creates_a_symlinked_directory(self):
        assert any(
            [path.isdir() and self.is_symlink_of_dotfiles_home(path)
             for path in test_home.children()])

    def dotfav_symlink_creates_a_symlink(self, src, dst):
        assert dst.islink()
        assert dst.realpath() == src

    def is_symlink_of_dotfiles_home(self, symlinkpath):
        return (symlinkpath.islink() and
                symlinkpath.realpath().startswith(test_dotfiles_home))


