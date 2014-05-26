# -*- coding: utf-8 -*-

import os

from dotfav.path import Path
import dotfav.config



class Unlink(object):
    def __init__(self, dotfiles, home):
        self._dotfiles = Path(dotfiles)
        self._home = Path(home)

        _dotfiles_home = self._dotfiles / 'home'
        self._files_in_dotfiles_home = list(_dotfiles_home.rglob('*'))

    def run(self):
        for unlinkable in self._iter_unlinkables_in_home():
            print('unlink: {}'.format(unlinkable))
            unlinkable.unlink()

    def _iter_unlinkables_in_home(self):
        return (f for f in self._home.iterdir() if self._is_unlinkable(f))

    def _is_unlinkable(self, f):
        return (f.is_symlink() and
                f.realpath in self._files_in_dotfiles_home)


def main(dotfiles=None, home=None):
    home = '~' if home is None else home
    config_path = Path(home) / '.dotfav' / 'config'
    config = dotfav.config.fromJsonFile(config_path)
    dotfiles = config.dotfiles if dotfiles is None else dotfiles

    command = Unlink(dotfiles, home)
    command.run()
