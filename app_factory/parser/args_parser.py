# -*- coding: utf-8 -*-
"""
Included generic argument parser, different apps parsers can use this parsers.
"""
import argparse
import glob
import os
import sys
from importlib import util


class BaseArgsParser(argparse.ArgumentParser):
    """
    Application specific parsers will inherit from this base parser in which error handling and basic parsing is set.
    """
    def __init__(self, *args, **kwargs):
        super(BaseArgsParser, self).__init__(*args, **kwargs)

    def add_sub_parsers(self):
        """
        Add sub-parsers for all the applications present.
        """
        subparsers = self.add_subparsers(help='sub-command help', dest='command')
        applications = glob.glob(os.path.join('*_app'))  # All application names will end with `_app`
        for app in applications:
            spec = util.spec_from_file_location("", os.path.join(f"{app}/utils/args_parser.py"))
            app_parser = util.module_from_spec(spec)
            spec.loader.exec_module(app_parser)
            app_parser.ParserHelper.add_arguments(subparsers)

    def error(self, message):
        """
        When an error will occur in any app's args this function will print help for that specific parser.
        :param message: Error message
        """
        sys.stderr.write('Error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)
