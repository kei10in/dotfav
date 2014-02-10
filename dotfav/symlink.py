# -*- coding: utf-8 -*-

import os
import sys
import json


class Environment(object):
    @property
    def repositorydir(self):
        return os.path.dirname(os.path.abspath(__file__))


class InstallCommandGenerator(object):
    def __init__(self, env, targets):
        self._env = env
        self._targets = targets

    def __iter__(self):
        for command in self._symlink_commands():
            yield command
    
    def _symlink_commands(self):
        for src, dst in self._targets:
            yield self._create_symlink_command(src, dst, os.path.isdir(src))

    def _create_symlink_command(self, src, dst, target_is_directory=False):
        source = os.path.join(self._env.repositorydir, src)
        destination = dst
        return SymlinkCommand(source, destination, target_is_directory)


class CommandError(Exception):
    def __init__(self, msg, real_exception=None):
        self.real_exception = real_exception
        
    def __str__(self):
        return str(self.real_exception)


class SymlinkCommand(object):
    def __init__(self, src, dst, target_is_directory=False):
        self.src = src
        self.dst = dst
        self.target_is_directory = target_is_directory

    @property
    def __src_fullpath(self):
        return os.path.expanduser(self.src.replace('/', os.path.sep))

    @property
    def __dst_fullpath(self):
        return os.path.expanduser(self.dst.replace('/', os.path.sep))

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
            os.symlink(self.__src_fullpath, self.__dst_fullpath, self.target_is_directory)
        else:
            os.symlink(self.__src_fullpath, self.__dst_fullpath)
        


class PlatformFilter(object):
    def __init__(self, platform=sys.platform):
        self._platform = platform

    def __iter__(self):
        return iter(list())

    def __call__(self, config):
        for c in config:
            if self._platform not in c['os']:
                continue
            for target in c['targets']:
                yield tuple(target)


def read_file(filepath):
    with open(filepath) as f:
        return f.read()


def main():
    env = Environment()
    config = json.loads(read_file('config.json'))
    filter = PlatformFilter()
    for command in InstallCommandGenerator(env, filter(config)):
        command.execute()
