"""Utils Module.

This module has differnet utility functions
"""
from datetime import datetime
import re


def get_weather_data_date(date_list, data_list, data):
    """Return weather data.

    This method extract date from the date list and
    return the date in words format
    """
    data_date = date_list[data_list.index(data)]
    return datetime.strptime(data_date, '%Y-%m-%d').strftime('%B %d')


def date_validation(date):
    """Validate Date.

    this meethod is for date validation format: 2014/12
    """
    regexp = re.compile(r'^[1-2][0-9]{3}/((0)?[1-9]|1[0-2])$')
    if regexp.search(str(date)):
        return
    print('Not a proper format or date')
    exit()


def year_validation(year):
    """Validate Year.

    This method is for year validation
    """
    regexp = re.compile(r'^[1-2][0-9]{3}$')
    if regexp.search(str(year)):
        return True
    return False
