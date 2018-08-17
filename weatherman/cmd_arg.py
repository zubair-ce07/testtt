""" This module is for validation of
the command line arguments recieved from the
terminal to programme
"""

import re


class CmdArg:
    """ This class contains methods
    to validate arguments recieved from the terminal
    like options and date
    """

    def __init__(self, option, date, path):
        self.option = option
        self.date = date
        self.error = ""

    def validate_arguments(self):

        """ This method validates the options and
        date format using regular expressions
        and sets error data member of class according
        to the validation
        :return:
        """

        if re.match('-[eacd]', self.option) is None:
            self.error = "Invalid option !!!"
            return
        date_format1 = re.match(r'^\d{4}$', self.date)
        date_format2 = re.match(r'^\d{4}/0?[1-9]$', self.date)
        date_format3 = re.match(r'^\d{4}/1[0-2]$', self.date)
        if self.option == '-e' and date_format1 is None:
            self.error = "option date mismatch !!!"
        elif self.option in 'acd' \
                and date_format2 is None and date_format3 is None:
            self.error = "option date mismatch !!!"
        elif date_format1 is None \
                and date_format2 is None and date_format3 is None:
            self.error = "Invalid date !!!"
        elif self.option != "-e" and date_format1 is not None:
            self.error = "option date mismatch !!!"

    def __str__(self):
        return ("Option: {}\nDate: {}\nError String: {}"
                .format(self.option, self.date, self.error))
