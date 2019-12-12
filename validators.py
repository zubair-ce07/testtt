import argparse
import os

from utilities import parse_date


def validate_arg_as_date(date_string):
    try:
        return parse_date(date_string, '%Y/%m')
    except ValueError:
        msg = f'Not a valid date: {date_string}. Acceptable format is YYYY/MM'
        raise argparse.ArgumentTypeError(msg)


def validate_arg_as_dir(path):
    if os.path.isdir(path):
        return path
    else:
        msg = f'dir_path:{path} is not a valid path'
        raise argparse.ArgumentTypeError(msg)
