# -*- coding: utf-8 -*-


class Either(object):
    pass


class Success(Either):
    def __init__(self, v):
        self.__v = v

    def bind(self, f, g):
        return f(self.__v)


class Fail(Either):
    def __init__(self, v):
        self.__v = v

    def bind(self, f, g):
        return g(self.__v)
