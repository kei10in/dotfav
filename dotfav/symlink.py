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


class HomeFileCollection(object):
    def __init__(self, src, dst, files):
        self._src = src
        self._dst = dst
        self._files = files

    def __iter__(self):
        files = self._files
        directories = (self._src, self._dst)
        return ((os.path.join(src, basename), os.path.join(dst, basename))
                for ((src, dst), basename) in product((directories, ), files))


class HomeFileSymlinkingCommands(object):
    def __init__(self, src, dst, files):
        self._src = src
        self._dst = dst
        self._files = files

    def __iter__(self):
        targets = HomeFileCollection(src=self._src, dst=self._dst, files=self._files)
        return iter(InstallCommandGenerator(targets))


class MappedFileCollection(object):
    def __init__(self, src, dst, mapped_files):
        self.__src = src
        self.__dst = dst
        self.__mapped_files = mapped_files

    def __iter__(self):
        for f, t in self.__mapped_files:
            yield os.path.join(self.__src, f), os.path.join(self.__dst, t)


class MappedFileSymlinkingCommands(object):
    def __init__(self, src, dst, config, platform):
        self._src = src
        self._dst = dst
        self._config = config
        self._platform = platform

    def __iter__(self):
        mapped_files = self.__reverse_inner_tuple(
            self.__filter_platform(self._config, self._platform))
        targets = MappedFileCollection(self._src, self._dst, mapped_files)
        return iter(InstallCommandGenerator(targets))

    @staticmethod
    def __reverse_inner_tuple(iterable):
        return (tuple(reversed(t)) for t in iterable)

    @staticmethod
    def __filter_platform(config, platform):
        return chain(*(c['target'].items() for c in config if platform in c['os']))


class Symlink(object):
    def __init__(self, dotfiles, home, platform):
        self._dotfiles = dotfiles
        self._home = home
        self._platform = platform

        self._config_file = os.path.join(self._dotfiles, 'dotfav.config')
        self._src = os.path.join(self._dotfiles, 'home')
        self._dst = self._home

    def run(self):
        commands = []

        files = self._list_home_targets()

        if files.is_success():
            commands.extend(self._home_file_symlinking_commands(files.value))
        else:
            print('`{}\': {}'.format(src, files.value.strerror), file=sys.stderr)
            sys.exit(1)

        if os.path.isfile(self._config_file):
            commands.extend(self._mapped_file_symlinking_commands())

        for command in commands:
            command.execute()

    def _home_file_symlinking_commands(self, files):
        return HomeFileSymlinkingCommands(self._src, self._dst, files)

    def _mapped_file_symlinking_commands(self):
        with open(self._config_file) as f:
            config = json.load(f)
            return MappedFileSymlinkingCommands(self._src,
                                                self._dst,
                                                config,
                                                self._platform)

    def _list_home_targets(self):
        try:
            return Success(os.listdir(self._src))
        except FileNotFoundError as e:
            return Fail(e)



def main(dotfiles=None, home=None, platform=None):
    dotfiles = '~/.dotfav/dotfiles' if dotfiles is None else dotfiles
    home = '~' if home is None else home
    platform = sys.platform if platform is None else platform

    command = Symlink(dotfiles, home, platform)
    command.run()
