""" This module conatins constants
of the program
"""


class Constants:
    """ This class contains the constants
    like RNF and FILE_PREFIX
    """

    # RNF = Record not founf
    RNF = "missing"
    FILE_PREFIX = "Murree_weather_"
    # IO exception
    IOE = "Something wrong while reading file\n" \
          "may be file does not exist"
    # invalid arguments
    IVA = "Invalid arguments !!!"
    # option and date mismatch
    O_MISS = "Option mismatch !!!"

    # Color codes
    END_COLR = '\33[0m'
    RED_COLR = '\33[31m'
    BLUE_COLR = '\33[34m'

    @staticmethod
    def get_rnf():
        """ this method returns RNF string
        :return:
        """

        return Constants.RNF

    @staticmethod
    def get_file_prefix():
        """ this method returns file_prefix
        :return:
        """

        return Constants.FILE_PREFIX
