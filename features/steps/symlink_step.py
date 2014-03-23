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
    assert dotfiles_home.is_dir()


@given('dotfiles home directory contains no files')
def step_impl(context):
    pass


@given('dotfiles home directory contains a file named "{filename}"')
def step_impl(context, filename):
    create_file_into_dotfiles_home(filename)


@given('dotfiles home directory contains a directory named "{dirname}"')
def step_impl(context, dirname):
    create_directory_into_dotfiles_home(dirname)


@given('dotfiles home directory contains a directory')
def step_impl(context):
    create_directory_into_dotfiles_home('directory')


@given('dotfiles contains config file')
def step_impl(context):
    create_config_file(context.text)


@when('we run dotfav symlink')
def step_impl(context):
    run_dotfav(command='symlink', home=str(home), dotfiles=str(dotfiles))


@when('we run dotfav symlink at platform "{platform}"')
def step_impl(context, platform):
    run_dotfav(command='symlink', home=str(home), dotfiles=str(dotfiles),
               platform=platform)


@then('no files are symlinked')
def step_impl(context):
    assert len([path for path in home.iterdir()
                if path.is_symlink()
                and path.resolve() in dotfiles_home.rglob('*')]) == 0


@then('"{name}" in home symlinks to "{target}" in dotfiles home')
def step_impl(context, name, target):
    path = home / name
    target_path = dotfiles_home / target
    assert path.is_symlink()
    assert path.resolve() == target_path


@then('"{filename}" in home is file')
def step_impl(context, filename):
    path = home / filename
    assert path.is_file()


@then('"{dirname}" in home is directory')
def step_impl(context, dirname):
    path = home / dirname
    assert path.is_dir()
