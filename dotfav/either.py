# -*- coding: utf-8 -*-


class Either(object):
    pass


class Success(Either):
    def __init__(self, v):
        self.value = v

    def is_success(self):
        return True

    def bind(self, f, g):
        return f(self.value)


class Fail(Either):
    def __init__(self, v):
        self.value = v

    def is_fail(self):
        return False

    def bind(self, f, g):
        return g(self.value)
