# -*- coding: utf-8 -*-

import os
import sys
import json
from itertools import product


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


class TargetFiles(object):
    def __init__(self, src, dst):
        self.__src = src
        self.__dst = dst

    def __iter__(self):
        files = os.listdir(self.__src)
        directories = (self.__src, self.__dst)
        return ((os.path.join(src, basename), os.path.join(dst, basename))
                for ((src, dst), basename) in product((directories, ), files))
        

def main(dotfiles):
    src = os.path.join(dotfiles, 'home')
    dst = '~'
    targets = TargetFiles(src=src, dst=dst)
    for command in InstallCommandGenerator(targets):
        command.execute()
