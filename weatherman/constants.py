"""
This module contains constants
of the program
"""


class Constants:
    """
    This class contains the constants
    like RNF and FILE_PREFIX
    """

    # RNF = Record not found
    RECORD_NOT_FOUND = "missing"
    FILE_PREFIX = "Murree_weather_"
    # IO exception
    IO_EXCEPTION = """Something wrong while reading file
                    \nmay be file does not exist"""
    # invalid arguments
    INVALID_ARGUMENTS = "Invalid arguments !!!"
    # option and date mismatch
    OPTION_DATE_MISMATCH = """Please check your options and date again 
                            \neither option or date is wrong!!!\nor may be both"""
    # invalid date
    INVALID_DATE = "Invalid Date !!!"

    # Color codes
    END_COLOR = '\33[0m'
    RED_COLOR = '\33[31m'
    BLUE_COLOR = '\33[34m'

    @staticmethod
    def get_rnf():
        """
        this method returns RNF string
        :return:
        """

        return Constants.RNF

    @staticmethod
    def get_file_prefix():
        """
        this method returns file_prefix
        :return:
        """

        return Constants.FILE_PREFIX
