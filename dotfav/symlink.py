# -*- coding: utf-8 -*-

import os
import sys
import json
from itertools import product
from itertools import chain

from dotfav.either import Success, Fail


class InstallCommandGenerator(object):
    def __init__(self, targets):
        self._targets = targets

    def __iter__(self):
        for command in self._symlink_commands():
            yield command

    def _symlink_commands(self):
        for src, dst in self._targets:
            yield self._create_symlink_command(src, dst)

    def _create_symlink_command(self, src, dst):
        return SymlinkCommand(src, dst)


class CommandError(Exception):
    def __init__(self, msg, real_exception=None):
        self.real_exception = real_exception
        
    def __str__(self):
        return str(self.real_exception)


class SymlinkCommand(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    @property
    def __src_fullpath(self):
        return self.__fullpath(self.src)

    @property
    def __dst_fullpath(self):
        return self.__fullpath(self.dst)

    def __fullpath(self, path):
        return os.path.abspath(os.path.expanduser(path.replace('/', os.path.sep)))

    def execute(self):
        msg = 'Create symbolic link from `{}\' to `{}\''
        print(msg.format(self.src, self.dst), file=sys.stderr)
        self.__do_symlink()

    def __do_symlink(self):
        try:
            if os.path.islink(self.__dst_fullpath):
                prompt = '`{}\' already exists. replace `{}\'? [yn]: '.format(
                    self.__dst_fullpath, self.__dst_fullpath)
                ans = input(prompt)
                if ans.lower().startswith('y'):
                    os.remove(self.__dst_fullpath)
                else:
                    return
            self.__symlink()
        except OSError as e:
            print('{}: {}'.format(self.dst, e.strerror), file=sys.stderr)

    def __symlink(self):
        if sys.platform == 'win32':
            target_is_directory = os.path.isdir(self.__src_fullpath)
            os.symlink(self.__src_fullpath, self.__dst_fullpath, target_is_directory)
        else:
            os.symlink(self.__src_fullpath, self.__dst_fullpath)


class TargetFileCollection(object):
    def __init__(self, src, dst, files):
        self.__src = src
        self.__dst = dst
        self.__files = files

    def __iter__(self):
        files = self.__files
        directories = (self.__src, self.__dst)
        return ((os.path.join(src, basename), os.path.join(dst, basename))
                for ((src, dst), basename) in product((directories, ), files))


def listdir(dirname):
    try:
        return Success(os.listdir(dirname))
    except FileNotFoundError as e:
        return Fail(e)


def symlink_home_files(src, dst, files):
    targets = TargetFileCollection(src=src, dst=dst, files=files)
    for command in InstallCommandGenerator(targets):
        command.execute()



class MappedTargetFileCollection(object):
    def __init__(self, src, dst, mapped_files):
        self.__src = src
        self.__dst = dst
        self.__mapped_files = mapped_files

    def __iter__(self):
        for f, t in self.__mapped_files:
            yield os.path.join(self.__src, f), os.path.join(self.__dst, t)


def symlink_mapped_files(src, dst, config_file, platform):
    with open(config_file) as f:
        config = json.load(f)
        mapped_files = reverse_inner_tuple(filter_platform(config, platform))
        targets = MappedTargetFileCollection(src, dst, mapped_files)
        for command in InstallCommandGenerator(targets):
            command.execute()


def reverse_inner_tuple(iterable):
    return (tuple(reversed(t)) for t in iterable)


def filter_platform(config, platform):
    return chain(*(c['target'].items() for c in config if platform in c['os']))


def main(dotfiles=None, home=None, platform=None):
    dotfiles = '~/.dotfav/dotfiles' if dotfiles is None else dotfiles
    home = '~' if home is None else home
    platform = sys.platform if platform is None else platform
    config_file = os.path.join(dotfiles, 'dotfav.config')

    src = os.path.join(dotfiles, 'home')
    dst = home
    files = listdir(src)

    def on_success(files):
        symlink_home_files(src, dst, files)

    def on_fail(e):
        print('`{}\': {}'.format(src, e.strerror), file=sys.stderr)

    files.bind(on_success, on_fail)

    if os.path.isfile(config_file):
        symlink_mapped_files(src, dst, config_file, platform)
