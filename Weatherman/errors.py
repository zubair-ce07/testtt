#!/usr/bin/python
class InvalidArguments(RuntimeError):
    
    def __init__(self, message):
        self.message = message
