# -*- coding: utf-8 -*-

import os

import pathlib


class Path(object):
    def __init__(self, s):
        self._org_path = str(s)
        self._path = pathlib.Path(os.path.expanduser(self._org_path))

    def __str__(self):
        return str(self._org_path)

    def __truediv__(self, other):
        if isinstance(other, Path):
            return Path(os.path.join(self._org_path, other._org_path))
        else:
            return Path(os.path.join(self._org_path, str(other)))

    @property
    def name(self):
        return self._path.name

    def exists(self):
        return self._path.exists()

    def is_file(self):
        return self._path.is_file()

    def is_dir(self):
        return self._path.is_dir()

    def is_symlink(self):
        return self._path.is_symlink()

    def iterdir(self):
        return map(lambda p: Path(p), self._path.iterdir())

    def symlink_to(self, target):
        target_is_directory = target.is_dir()
        return self._path.absolute().symlink_to(target._path.absolute(), target_is_directory)

    def unlink(self):
        return self._path.unlink()

    def open(self, *args, **kwds):
        return self._path.open(*args, **kwds)
