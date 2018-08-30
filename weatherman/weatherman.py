"""
This is the main module of
the program from here the program
initiates its execution and prints
results of temperatures according to
the given options and date
"""

import sys
import calendar

from command_arguments import CommandArgument
from csv_file_content import FileContent
from constants import Constants
from helpers import *


def __main__():
    """
    This is the entry point of the
    program. this function just calls different functions
    on the basis of some checks
    :return:
    """
    
    arguments = {}
    manage_arguments(arguments)
    file_content = FileContent(arguments["path"])
    for i in range(1, arguments["total_options"] + 1):
        if arguments["option{}".format(i)] == '-e':
            get_output_for_e_option(file_content, arguments["date{}".format(i)])
        elif arguments["option{}".format(i)] == '-a':
            get_output_for_a_option(file_content, arguments["date{}".format(i)])
        elif arguments["option{}".format(i)] == '-c':
            get_output_for_c_option(file_content, arguments["date{}".format(i)])
        elif arguments["option{}".format(i)] == '-d':
            get_output_for_d_option(file_content, arguments["date{}".format(i)])


def manage_arguments(arguments):
    """
    This function just manage all the
    validations of the input cmd arguments
    if arguments will be wrong it will
    print a message and terminate the program
    :param arguments:
    :return:
    """

    arguments["total"] = len(sys.argv)
    if arguments["total"] < 4 or arguments["total"] % 2 != 0:
        print(Constants.INVALID_ARGUMENTS)
        exit(1)
    arguments["path"] = sys.argv[1]
    i = 2
    j = 1
    while i < arguments["total"]:
        arguments["option{}".format(j)] = sys.argv[i]
        arguments["date{}".format(j)] = sys.argv[i + 1]
        j += 1
        i += 2
    arguments["total_options"] = j - 1

    j = 1
    while j <= arguments["total_options"]:
        my_arguments = CommandArgument(arguments["option{}".format(j)],
                                       arguments["date{}".format(j)])
        my_arguments.validate_arguments()
        if my_arguments.error != "":
            print(my_arguments.error)
            exit(1)
        j += 1


def get_output_for_a_option(file_content, date):
    """
    This function displays the
    average of highest temperature,
    average of lowest temperature
    average of highest humidity of
    the given month of a year
    :param file_content:
    :param date:
    :return:
    """

    month_abbreviation, month, year = split_date(date)
    monthly_temp_humidity_avg = file_content.get_average_monthly_data(year, month_abbreviation)
    if monthly_temp_humidity_avg is None:
        print(Constants.IO_EXCEPTION)
        return
    print("Highest Average: {:02d}C".format(monthly_temp_humidity_avg["max_temp_avg"]))
    print("Lowest Average: {:02d}C".format(monthly_temp_humidity_avg["min_temp_avg"]))
    print("Average Mean Humidity: {:02d}%\n".format(monthly_temp_humidity_avg["mean_humidity_avg"]))


def get_output_for_e_option(file_content, date):
    """
    This function displays the
    yearly report of highest temperature,
    lowest temperature and highest humidity
    :param file_content:
    :param date:
    :return:
    """

    yearly_temp_humidity = file_content.get_yearly_data(date)
    if yearly_temp_humidity is None:
        print(Constants.IO_EXCEPTION)
        return
    if not yearly_temp_humidity["file_found"]:
        print(Constants.IO_EXCEPTION)
        return

    max_temp_date = yearly_temp_humidity["max_temp_year"].split('-')
    min_temp_date = yearly_temp_humidity["min_temp_year"].split('-')
    max_humidity_date = yearly_temp_humidity["max_humidity_year"].split('-')
    print("Highest: {:02d}C on {} {}".format(
        yearly_temp_humidity["max_temp"],
        calendar.month_name[int(max_temp_date[1])],
        max_temp_date[2]
    ))
    print("Lowest: {:02d}C on {} {}".format(
        yearly_temp_humidity["min_temp"],
        calendar.month_name[int(min_temp_date[1])],
        min_temp_date[2]
    ))
    print("Humidity: {:02d}% on {} {}\n".format(
        yearly_temp_humidity["max_humidity"],
        calendar.month_name[int(max_humidity_date[1])],
        max_humidity_date[2]
    ))


def get_output_for_c_option(file_content, date):
    """
    This method displays the bar chart
    representation of highest and lowest
    temperatures of the given month of the year
    on separate lines with red + for high
    and blue + for low
    :param file_content:
    :param date:
    :return:
    """

    month_abbreviation, month_name, year = split_date(date)
    daily_temps_of_month = file_content.get_daily_temps_of_month(year, month_abbreviation)
    if daily_temps_of_month is None:
        print(Constants.IO_EXCEPTION)
        return
    print(month_name, year)
    i = 1
    while i <= len(daily_temps_of_month[0]):
        print("{}{:02d} ".format(Constants.END_COLOR, i), end="")
        if daily_temps_of_month[0][i] == Constants.RECORD_NOT_FOUND:
            print("{}missing".format(Constants.RED_COLOR))
        else:
            temperature = daily_temps_of_month[0][i]
            symbol = '+'
            set_printing_symbol_and_temp(symbol, temperature)
            print("{}{}".format(Constants.RED_COLOR, symbol) * temperature, end="")
            print("{} {:02d}C".format(Constants.END_COLOR, daily_temps_of_month[0][i]))
        print("{}{:02d} ".format(Constants.END_COLOR, i), end="")
        if daily_temps_of_month[1][i] == Constants.RECORD_NOT_FOUND:
            print("{}missing".format(Constants.BLUE_COLOR))
        else:
            temperature = daily_temps_of_month[1][i]
            symbol = '+'
            set_printing_symbol_and_temp(symbol, temperature)
            print("{}{}".format(Constants.BLUE_COLOR, symbol) * temperature, end="")
            print("{} {:02d}C".format(Constants.END_COLOR, daily_temps_of_month[1][i]))
        i += 1
    print(Constants.END_COLOR, end="")


def get_output_for_d_option(file_content, date):
    """
    This method displays the bar chart
    representation of highest and lowest
    temperatures of the given month of the year
    on single line with red + for high
    and blue + for low
    :param file_content:
    :param date:
    :return:
    """

    month_abbreviation, month_name, year = split_date(date)
    daily_temps_of_month = file_content.get_daily_temps_of_month(year, month_abbreviation)
    if daily_temps_of_month is None:
        print(Constants.IO_EXCEPTION)
        return
    print(month_name, year)
    i = 1
    while i <= len(daily_temps_of_month[0]):
        high_temp_missed = (daily_temps_of_month[0][i] == Constants.RECORD_NOT_FOUND)
        low_temp_missed = (daily_temps_of_month[1][i] == Constants.RECORD_NOT_FOUND)
        print("{}{:02d} ".format(Constants.END_COLOR, i), end="")
        if high_temp_missed:
            print("{}missing".format(Constants.RED_COLOR), end="")
        else:
            temperature = daily_temps_of_month[0][i]
            symbol = '+'
            set_printing_symbol_and_temp(symbol, temperature)
            print("{}{}".format(Constants.RED_COLOR, symbol) * temperature, end="")
        if low_temp_missed:
            print("{}missing".format(Constants.BLUE_COLOR), end="")
        else:
            temperature = daily_temps_of_month[1][i]
            symbol = '+'
            set_printing_symbol_and_temp(symbol, temperature)
            print("{}{}".format(Constants.BLUE_COLOR, symbol) * temperature, end="")
        if high_temp_missed:
            print("{} missing-".format(Constants.RED_COLOR), end="")
        else:
            print("{} {:02d}C-"
                  .format(Constants.END_COLOR, daily_temps_of_month[0][i]), end="")
        if low_temp_missed:
            print("{}missing".format(Constants.BLUE_COLOR))
        else:
            print("{}{:02d}C".format(Constants.END_COLOR, daily_temps_of_month[1][i]))
        i += 1
    print(Constants.END_COLOR, end="")


if __name__ == "__main__":
    __main__()
