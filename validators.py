import argparse
import os
from datetime import datetime


def validate_arg_as_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y/%m')
    except ValueError:
        msg = f'Not a valid date: {date_string}. Acceptable format is YYYY/MM'
        raise argparse.ArgumentTypeError(msg)


def validate_arg_as_year(date_string):
    try:
        return datetime.strptime(date_string, '%Y').year
    except ValueError:
        msg = f'Not a valid year: {date_string}. Acceptable format is YYYY'
        raise argparse.ArgumentTypeError(msg)


def validate_arg_as_dir(path):
    if os.path.isdir(path):
        return path
    else:
        msg = f'dir_path:{path} is not a valid path'
        raise argparse.ArgumentTypeError(msg)
