"""
Main module which runs the whole weatherman program, It takes Command Line Args to work with

Command Line Args:
'-e' : Gives highest, lowest temperatures and highest humidity
'-a' : Gives average temperature and humidity
'-c' : Gives results in the chart/graph form
'-d' : Gives results in chart form but 1 day has only 1 graph
"""

import sys

from CalculationModule import calculator
from ParserModule import parser_


def is_even(num):
    return num % 2 == 0


def main_function():
    """Takes system args and extract options and time to iterate the whole process over it"""
    if is_even(len(sys.argv)):
        path_dir = sys.argv[1]
        values = sys.argv[2:]
        for i in range(0, len(values), 2):
            option = values[i]
            time_span = values[i + 1]

            data_set = parser_(path_dir, time_span)
            if data_set is not None:
                calculator(time_span, option, data_set)
            else:
                print("\nThe given Time Span : {0} is not valid\n".format(time_span))
    else:
        print("\nThe arguments are not complete")


if __name__ == "__main__":
    main_function()
