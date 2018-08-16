"""
Main module which runs the whole weatherman program, It takes Command Line Args to work with

Command Line Args:
'-e' : Gives highest, lowest temperatures and highest humidity
'-a' : Gives average temperature and humidity
'-c' : Gives results in the chart/graph form
'-d' : Gives results in chart form but 1 day has only 1 graph showing range of temperature
"""

import sys

import CalculationModule
from ParserModule import parser


def is_even(num):
    return num % 2 == 0


_function_specifier = {
    '-e': CalculationModule.extreme_temperature_conditions,
    '-a': CalculationModule.average_temperature_conditions,
    '-c': CalculationModule.chart_highest_lowest_temperature,
    '-d': CalculationModule.temperature_range_chart,
}


def main_function():
    """Takes system args and extract options and time to iterate the whole process over it"""
    if is_even(len(sys.argv)) and len(sys.argv) > 2:
        directory_path = sys.argv[1]
        values = sys.argv[2:]
        for i in range(0, len(values), 2):
            option = values[i]
            time_span = values[i + 1]

            data_set = parser(directory_path, time_span)

            if data_set and option in _function_specifier.keys():
                _function_specifier[option](time_span, data_set)

            else:
                print("\nThe given Time Span or Option is not valid\n")
    else:
        print("\nThe arguments are not complete")


if __name__ == "__main__":
    main_function()
