# -*- coding: utf-8 -*-

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

    def given_there_are_dotfiles_home_directory_in_dotfiles(self):
        create_test_temp_directories()
        assert test_dotfiles_home.isdir()

    def when_dotfiles_home_directory_contains_no_files(self):
        pass

    def when_dotfiles_home_directory_contains_a_file(self):
        create_file_into_dotfiles_home('file')

    def when_dotfiles_home_directory_contains_a_directory(self):
        create_directory_into_dotfiles_home('file')

    def run_dotfav_symlink(self):
        dotfav.main('dotfav symlink --home {} --dotfiles {}'.format(
            test_home, test_dotfiles).split())

    def no_files_are_symlinked(self):
        assert len([path for path in test_home.children()
                    if path.islink()
                    and path.realpath().startswith(test_dotfiles_home)]) == 0

    def dotfav_symlink_creates_a_symlinked_file(self):
        assert len([path for path in test_home.children()
                    if path.islink()
                    and path.isfile()
                    and path.realpath().startswith(test_dotfiles_home)]) == 1

    def dotfav_symlink_creates_a_symlinked_directory(self):
        assert len([path for path in test_home.children()
                    if path.islink()
                    and path.isdir()
                    and path.realpath().startswith(test_dotfiles_home)]) == 1

