# -*- coding: utf-8 -*-
"""
Included generic argument parser, different apps parsers can use this parsers.
"""
import argparse
import glob
import importlib
import os
import sys


class BaseArgsParser(argparse.ArgumentParser):
    """
    Application specific parsers will inherit from this base parser in which error handling and basic parsing is set.
    """
    def __init__(self, *args, **kwargs):
        super(BaseArgsParser, self).__init__(*args, **kwargs)

    def add_sub_parser_of_applications(self):
        subparsers = self.add_subparsers(help='sub-command help', dest='command')
        p = subparsers.add_parser(name='a')
        p.add_argument(
            "-c",
            "--md",
            help="s",
            type=str
        )
        applications = glob.glob(os.path.join('*_app'))  # All application names will end with `_app`
        for app in applications:
            spec = importlib.util.spec_from_file_location("", os.path.join(f"{app}/utils/args_parser.py"))
            app_parser = importlib.util.module_from_spec(spec)
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
