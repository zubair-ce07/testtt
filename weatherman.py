"""
Main module which runs the whole weatherman program, It takes Command Line Args to work with

Command Line Args:
'-e' : Gives highest, lowest temperatures and highest humidity
'-a' : Gives average temperature and humidity
'-c' : Gives results in the chart/graph form
'-r' : Gives results in chart form but 1 day has only 1 graph showing range of temperature
"""

import sys

import CalculationModule
from ParserModule import parser


def is_even(num):
    return num % 2 == 0


def main_function():
    """Takes system args and extract options and time to iterate the whole process over it"""
    if is_even(len(sys.argv)):
        directory_path = sys.argv[1]
        values = sys.argv[2:]
        for i in range(0, len(values), 2):
            option = values[i]
            time_span = values[i + 1]

            data_set = parser(directory_path, time_span)
            if data_set is not None:

                # -e  option will give highest, lowest temperature statistics of records
                if option == "-e":
                    CalculationModule.extreme_temperature_conditions(time_span, data_set)

                # -a option will give average statistics of records
                elif option == "-a":
                    CalculationModule.average_temperature_conditions(time_span, data_set)

                # -c option will give horizontal chart bar
                elif option == "-c":
                    CalculationModule.chart_highest_lowest_temperature(time_span, data_set)

                # -d option will give horizontal chart bar of each day defining lowest and highest temperatures
                elif option == "-d":
                    CalculationModule.temperature_range_chart(time_span, data_set)

                else:
                    print("The Given Option is not valid")
            else:
                print(f"\nThe given Time Span : {time_span} is not valid\n")
    else:
        print("\nThe arguments are not complete")


if __name__ == "__main__":
    main_function()
