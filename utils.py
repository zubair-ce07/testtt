"""
this module has all the utility functions of program
"""

import re


def validate_date_str(date_str, option):
    """
    this functon validates date string that we get from input
    :param date_str:
    :param option:
    :return:
    """
    # for comparing date string of the form 'YYYY' OR 'YYYY/MM'
    if option == 0:
        return bool(re.search(r"^\d{4}(([/])(0?[1-9]|1[012]))?$", date_str))

    # for comparing date string of the form 'YYYY/MM' only
    elif option == 1:
        return bool(re.search(r"^\d{4}([/])(0?[1-9]|1[012])$", date_str))

    return True


weather_data = []
