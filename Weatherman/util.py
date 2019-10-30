"""This module provide the helping functions"""
import argparse
from os import path
from datetime import datetime


def format_header(header):
    """strip list of strings, replace spaces with _ and convert it to lowercase"""
    return header.strip().replace(" ", "_").lower()


def get_date_pattern(date):
    """parse the given data and return the start and end date with read_type"""
    if "/" in date:
        year, month = date.split("/")
        date = datetime(int(year), int(month), 1)
        date_pattern = date.strftime('%Y_%b')
    else:
        date = datetime(int(date), 1, 1)
        date_pattern = date.strftime('%Y*')
    return date_pattern


def validate_path(value):
    """Check if path is valid"""
    if not path.exists(value):
        raise argparse.ArgumentTypeError("%s is an invalid file path" % value)
    return value


def validate_year(value):
    """ validate year """
    datetime(int(value), 1, 1)
    return value


def validate_year_month(value):
    """ validate year and month passed """
    error = argparse.ArgumentTypeError(
        "%s invalid date format. Enter as YEAR/MON" % value)
    if len(value.split("/")) == 1:
        raise error
    splited_val = value.split("/")
    datetime(int(splited_val[0]), int(splited_val[1]), 1)

    return value
