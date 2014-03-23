# -*- coding: utf-8 -*-

import shutil

from utils import *


def cleanup_temp_directory():
    if test_temp.is_dir():
        shutil.rmtree(str(test_temp))
    elif test_temp.is_file():
        test_temp.unlink()


@given('there are dotfiles home directory in dotfiles')
def step_impl(context):
    cleanup_temp_directory()
    create_test_temp_directories()
    assert test_dotfiles_home.is_dir()


@given('dotfiles home directory contains no files')
def step_impl(context):
    pass


@given('dotfiles home directory contains a file')
def step_impl(context):
    create_file_into_dotfiles_home('file')


@given('dotfiles home directory contains a directory')
def step_impl(context):
    create_directory_into_dotfiles_home('directory')


@given('dotfiles contains config file')
def step_impl(context):
    create_config_file(context.text)


@given('dotfiles home directory contains a file named "{filename}"')
def step_impl(context, filename):
    create_file_into_dotfiles_home(test_dotfiles_home / filename)


@when('we run dotfav symlink')
def step_impl(context):
    run_dotfav(command='symlink', home=str(test_home), dotfiles=str(test_dotfiles))


@when('we run dotfav symlink at platform "{platform}"')
def step_impl(context, platform):
    run_dotfav(command='symlink', home=str(test_home), dotfiles=str(test_dotfiles),
               platform=platform)


@then('no files are symlinked')
def step_impl(context):
    assert len([path for path in test_home.iterdir()
                if path.is_symlink()
                and path.resolve() in test_dotfiles_home.rglob('*')]) == 0


@then('dotfav symlink creates a symlinked file')
def step_impl(context):
    assert any([path.is_file() and is_symlink_of_dotfiles_home(path)
                for path in test_home.iterdir()])


@then('dotfav symlink creates a symlinked directory')
def step_impl(context):
    assert any([path.is_dir() and is_symlink_of_dotfiles_home(path)
                for path in test_home.iterdir()])


@then('dotfav symlink creates a symlink "{src}" to "{dst}"')
def step_impl(context, src, dst):
    src = test_dotfiles_home / src
    dst = test_home / dst
    assert dst.is_symlink()
    assert dst.resolve() == src


def is_symlink_of_dotfiles_home(path):
    return (path.is_symlink() and path.resolve() in test_dotfiles_home.rglob('*'))
