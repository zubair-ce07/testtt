#!/usr/bin/python
class InvalidArguments(RuntimeError):

    "This class is used for notifying invalid arguments"
    def __init__(self, message):
        self.message = message
