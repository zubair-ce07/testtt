"""
Module handles all the aspects of color printing on terminals
"""


class ColorPrint:
    """
    Responsible for providing different methods to assist in
    printing on terminals in color. Currently it supports only
    Red and Blue.

    Since the class itself has no state and is a utility class
    so all methods are declared as static
    """

    @staticmethod
    def red(input_str):
        """
        Prints the input_str in red color

        Arguments:
            input_str(str): input in string format
        """

        # \33[31;0m is the starting code for red color in ANSI standard
        # \33[0m is the ending code for red color in ANSI standard
        # still researching on this color code
        print('\33[31;0m'+input_str+'\33[0m')

    @staticmethod
    def red_raw(input_str):
        """
        Returns the input_str in red color

        Arguments:
            input_str(str): input in string format

        Returns:
            (str): input_str in red color
        """

        return '\33[31;0m'+input_str+'\33[0m'

    @staticmethod
    def blue(input_str):
        """
        Prints the input_str in blue color

        Arguments:
            input_str(str): input in string format
        """

        print('\33[34;0m'+input_str+'\33[0m')

    @staticmethod
    def blue_raw(input_str):
        """
        Returns the input_str in blue color

        Arguments:
            input_str(str): input in string format

        Returns:
            (str): input_str in blue color
        """

        return '\33[34;0m' + input_str + '\33[0m'
