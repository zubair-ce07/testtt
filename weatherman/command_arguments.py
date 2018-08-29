"""
This module is for validation of
the command line arguments received from the
terminal to programme
"""

import re

from constants import Constants


class CommandArgument:
    """
    This class contains methods
    to validate arguments received from the terminal
    like options and date
    """

    def __init__(self, option, date):
        self.option = option
        self.date = date
        self.error = ""

    def validate_arguments(self):
        """
        This method validates the options and
        date format using regular expressions
        and sets error data member of class according
        to the validation
        :return:
        """

        my_string = '{} {}'.format(self.option, self.date)
        regex = '(-e \d{4})|((-[acd] \d{4}\/)((1[0-2])|(0?[1-9])))'
        match_object = re.match(regex, my_string)
        if match_object is None or match_object.span()[1] != len(my_string):
            self.error = "{}\n{}".format(Constants.INVALID_ARGUMENTS,
                                         Constants.OPTION_DATE_MISMATCH)
            return

    def __str__(self):
        return ("Option: {}\nDate: {}\nError String: {}"
                .format(self.option, self.date, self.error))
