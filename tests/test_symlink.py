# -*- coding: utf-8 -*-

import shutil

from utils import *


class TestScenario1(object):
    def setup_method(self, method):
        if test_temp.is_dir():
            shutil.rmtree(str(test_temp))
        elif test_temp.is_file():
            test_temp.unlink()

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

    def test_symlink_with_config_file(self):
        self.given_there_are_dotfiles_home_directory_in_dotfiles()
        self.when_dotfiles_contains_config_file([{
                'os': ['darwin'],
                'target': {'file': 'file.darwin'}
            }])
        self.when_dotfiles_home_directory_contains_a_file_named('file.darwin')
        self.run_dotfav_symlink_at_platform('darwin')
        self.dotfav_symlink_creates_a_symlink(
            test_dotfiles_home / 'file.darwin',
            test_home / 'file')

    def given_there_are_dotfiles_home_directory_in_dotfiles(self):
        create_test_temp_directories()
        assert test_dotfiles_home.is_dir()

    def when_dotfiles_contains_config_file(self, config):
        create_config_file(config)

    def when_dotfiles_home_directory_contains_no_files(self):
        pass

    def when_dotfiles_home_directory_contains_a_file(self):
        self.when_dotfiles_home_directory_contains_a_file_named('file')

    def when_dotfiles_home_directory_contains_a_file_named(self, name):
        create_file_into_dotfiles_home(name)

    def when_dotfiles_home_directory_contains_a_directory(self):
        create_directory_into_dotfiles_home('directory')

    def run_dotfav_symlink(self):
        run_dotfav(command='symlink', home=str(test_home), dotfiles=str(test_dotfiles))

    def run_dotfav_symlink_at_platform(self, platform):
        run_dotfav(command='symlink', home=str(test_home), dotfiles=str(test_dotfiles),
                   platform=platform)

    def no_files_are_symlinked(self):
        assert len([path for path in test_home.iterdir()
                    if path.is_symlink()
                    and path.resolve() in test_dotfiles_home.rglob('*')]) == 0

    def dotfav_symlink_creates_a_symlinked_file(self):
        assert any(
            [path.is_file() and self.is_symlink_of_dotfiles_home(path)
             for path in test_home.iterdir()])

    def dotfav_symlink_creates_a_symlinked_directory(self):
        assert any(
            [path.is_dir() and self.is_symlink_of_dotfiles_home(path)
             for path in test_home.iterdir()])

    def dotfav_symlink_creates_a_symlink(self, src, dst):
        assert dst.is_symlink()
        assert dst.resolve() == src

    def is_symlink_of_dotfiles_home(self, symlinkpath):
        return (symlinkpath.is_symlink() and
                symlinkpath.resolve() in test_dotfiles_home.rglob('*'))
