"""
This module contains the helper
functions which will be used
by other functions
"""

import re
import calendar


def is_num(value):
    """
    This function checks either
    string contains a number or not
    :param value:
    :return:
    """

    regex = "-?[\d]*"
    if value == '' or re.match(regex, value) is None:
        return False
    else:
        return True


def split_date(date):
    """
    this function gets date in string
    and returns month abbreviation, month name and year
    :param date:
    :return:
    """

    date_tokens = date.split("/")
    year = date_tokens[0]
    month_abbreviation = calendar.month_abbr[int(date_tokens[1])]
    month_name = calendar.month_name[int(date_tokens[1])]
    return month_abbreviation, month_name, year


def set_printing_symbol_and_temp(symbol, temperature):
    """
    This function sets printing symbol and
    temperature according to positive or
    negative value
    :param symbol:
    :param temperature:
    :return:
    """

    temperature = int(temperature)
    symbol = '+'
    if temperature < 0:
        symbol = '-'
        temperature *= -1
