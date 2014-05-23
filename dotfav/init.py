# -*- coding: utf-8 -*-

import json

from dotfav.path import Path


class Iinitialize(object):
    def __init__(self, default_dotfiles, home):
        self._default_dotfiles = Path(default_dotfiles)
        self._config_path = Path(home) / '.dotfav' / 'config'

    def run(self):
        config = { 'dotfiles': str(self._default_dotfiles) }
        with self._config_path.open('w') as f:
            json.dump(config, f)


def main(default_dotfiles, home=None):
    home = '~' if home is None else home
    command = Iinitialize(default_dotfiles, home)
    command.run()


