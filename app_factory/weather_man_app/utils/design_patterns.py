# -*- coding: utf-8 -*-
"""
This file included design pattern base classes (Which are required explicitly). Other design patterns are implemented
in application as well.
"""


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        """
        Checks weather an instance of this class is already created or not, return same instance if already is created
        somewhere or returns new instance.
        :param args:
        :param kwargs:
        :return:
        """
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
