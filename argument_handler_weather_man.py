from __future__ import print_function

import sys


class ArgumentHandler:
    """This class contains methods to handle the arguments by the user
    at the terminal. It refines the input into separate entities
    to be used by other functions.
    methods: year_month_handler
             multiple_arguments
    :result processed input stored in specific variables"""

    def __init__(self):
        """This __init__ function gets the input from the terminal using .sys
        library and stores them into predefined variables for further
        processing.
        :param sys.argv[] : All the inputs from the terminal are stored here
                            and passed as parameters to this function.
        :returns number_of_arguments : total number of arguments passed
                 path_file : directory path of the weather files
                 mode : flag set for calculations
                 year_date : year and month for calculation"""
        self.number_of_arguments = len(sys.argv)
        self.path_file = sys.argv[1]
        self.mode = sys.argv[2]
        self.year_date = str(sys.argv[3])
        self.year = 0
        self.month = 0
        self.multiple = self.number_of_arguments

    def year_month_handler(self):
        """This function breaks down the string of month and date into each
        variable. It also handles the case for more than flags passed
        :param year_date[] : time info passed at the terminal
        :return: year : year for calculation in numeric
                 month : specific month in numeric
        """
        self.year = self.year_date[:4]
        self.month = self.year_date[5:]

        if self.month is '':
            self.month = 0

    def multiple_arguments(self):
        """This is a function to return the total number of arguments which
        will be used in the main function to handle multiple flags
        :returns multiple : how many total arguments passed
        """
        if self.number_of_arguments > 4:
            return self.multiple
