# -*- coding: utf-8 -*-

import sys
import argparse

import dotfav.symlink
import dotfav.unlink

__version__ = '0.1'

class DotFav(object):
    def __init__(self, argv=sys.argv):
        parser = DotFav.argument_parser()
        if len(argv) < 2:
            self._args = parser.parse_args(['help'])
        else:
            self._args = parser.parse_args(argv[1:])

    @staticmethod
    def argument_parser():
        parser = argparse.ArgumentParser(description='manage dotfiles.')
        subparsers = parser.add_subparsers(title='subcommands',
                                           description='dotfav subcommands')

        parser_help = subparsers.add_parser('help', help='show help')
        parser_help.set_defaults(func=parser.print_help)

        parser_symlink = subparsers.add_parser('symlink', help='create symbolic links')
        parser_symlink.set_defaults(func=DotFav.symlink)
        parser_symlink.add_argument('--dotfiles', help='specify dotfiles directory')
        parser_symlink.add_argument('--home', help='specify home directory')
        parser_symlink.add_argument('--platform', help='specify platform')

        parser_unlink = subparsers.add_parser('unlink', help='remove symlinked files')
        parser_unlink.set_defaults(func=DotFav.unlink)
        parser_unlink.add_argument('--dotfiles', help='specify dotfiles directory')
        parser_unlink.add_argument('--home', help='specify home directory')
        parser_unlink.add_argument('--platform', help='specify platform')

        return parser

    @staticmethod
    def symlink(dotfiles=None, home=None, platform=None, **kwds):
        dotfav.symlink.main(dotfiles, home, platform)

    @staticmethod
    def unlink(dotfiles=None, home=None, **kwds):
        dotfav.unlink.main(dotfiles, home)

    def run(self):
        self._args.func(**vars(self._args))
        

def main(argv=sys.argv):
    try:
        DotFav(argv).run()
        return 0
    except KeyboardInterrupt:
        return 1
