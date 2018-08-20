"""
This module contains the helper
functions which will be used
by other functions
"""

import re

def is_num(value):
    """
    This function checks either
    string contains a number or not
    :param str_:
    :return:
    """

    regex = "-?[\d]*"
    if value == '' or re.match(regex, value) is None:
        return False
    else:
        return True
