from argparse import ArgumentParser
import sys
import os
import datetime


class My_ArgParser(ArgumentParser):

    def __init__(self):
        super().__init__(description='Task 1 the Weather Man')
        self.my_add_args()
        self.args = self.parse_args(sys.argv)

    def my_add_args(self):
        self.add_argument(
            'file_name',
            help='name of file')
        self.add_argument(
            'path',
            help='Path to Dir')
        self.add_argument(
            '-a',
            action='store',
            type=lambda s: datetime.datetime.strptime(s, '%Y/%m').date(),
        )
        self.add_argument(
            '-c',
            action='store',
            type=lambda s: datetime.datetime.strptime(s, '%Y/%m').date(),
        )
        self.add_argument(
            '-e',
            action='store',
            type=lambda s: datetime.datetime.strptime(s, '%Y').date(),
        )
