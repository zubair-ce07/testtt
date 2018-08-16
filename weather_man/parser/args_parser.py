# -*- coding: utf-8 -*-
"""
Included generic argument parser, different apps parsers can use this parsers.
"""
import argparse
import sys


class BaseArgsParser(argparse.ArgumentParser):
    """
    Application specific parsers will inherit from this base parser in which error handling and basic parsing is set.
    """
    def __init__(self, *args, **kwargs):
        super(BaseArgsParser, self).__init__(*args, **kwargs)

    def error(self, message):
        """
        When an error will occur in any app's args this function will print help for that specific parser.
        :param message: Error message
        """
        sys.stderr.write('Error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)
