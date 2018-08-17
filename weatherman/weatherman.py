""" This is the main module of
the program from here the program
initiates its execution and prints
results of temperatures according to
the given options and date
"""

import sys
import calendar

from cmd_arg import CmdArg
from csv_file_content import FileContent
from constants import Constants


def __main__():
    """ This is the entry point of the
    program. this function just calls different functions
    on the basis of some checks
    :return:
    """
    arguments = {}
    manage_arguments(arguments)
    file_cont = FileContent(arguments["path"])
    if arguments["total_arg"] == 8:
        get_special_report(file_cont, arguments)
    else:
        if arguments["option"] == '-e':
            get_output_for_e_option(file_cont, arguments["date"])
        elif arguments["option"] == "-a":
            get_output_for_a_option(file_cont, arguments["date"])
        elif arguments["option"] == '-c':
            get_output_for_c_option(file_cont, arguments["date"])
        elif arguments["option"] == '-d':
            get_output_for_d_option(file_cont, arguments["date"])


def manage_arguments(arguments):
    """ This function just manage all the
    validations of the input cmd arguments
    if arguments will be wrong it will
    print a message and terminate the program
    :param arguments:
    :return:
    """

    arguments["total_arg"] = len(sys.argv)

    if arguments["total_arg"] == 8:
        arguments["path"] = sys.argv[1]
        arguments["option1"] = sys.argv[2]
        arguments["date1"] = sys.argv[3]
        arguments["option2"] = sys.argv[4]
        arguments["date2"] = sys.argv[5]
        arguments["option3"] = sys.argv[6]
        arguments["date3"] = sys.argv[7]

        if arguments["option1"] != "-c" or \
                arguments["option2"] != "-a" or \
                arguments["option3"] != "-e":
            print(Constants.O_MISS)
            exit(1)

        cmd_arg = CmdArg(arguments["option1"], arguments["date1"])
        if cmd_arg.error != "":
            print(cmd_arg.error)
            exit(1)
        cmd_arg = CmdArg(arguments["option2"], arguments["date2"])
        if cmd_arg.error != "":
            print(cmd_arg.error)
            exit(1)
        cmd_arg = CmdArg(arguments["option3"], arguments["date3"])
        if cmd_arg.error != "":
            print(cmd_arg.error)
            exit(1)
        return

    if arguments["total_arg"] != 4:
        print(Constants.IVA)
        exit(1)
    else:
        arguments["path"] = sys.argv[1]
        arguments["option"] = sys.argv[2]
        arguments["date"] = sys.argv[3]
        cmd_arguments = CmdArg(arguments["option"], arguments["date"])
        cmd_arguments.validate_arguments()

        if cmd_arguments.error != "":
            print(cmd_arguments.error)
            exit(1)


def get_special_report(file_cont, arguments):
    """ This function will dispaly the
    special report i.e. yearly, monthly average
    and monthly highest temperature and humidity
    :param file_cont:
    :param arguments:
    :return:
    """

    get_output_for_c_option(file_cont, arguments["date1"])
    print("")
    get_output_for_a_option(file_cont, arguments["date2"])
    print("")
    get_output_for_e_option(file_cont, arguments["date3"])


def get_output_for_a_option(file_cont, date):
    """ This function displays the
    average of highest temperature,
    average of lowest temperature
    average of highest humidity of
    the given month of a year
    :param file_cont:
    :param date:
    :return:
    """

    date_tokens = date.split("/")
    year = date_tokens[0]
    month = calendar.month_abbr[int(date_tokens[1])]
    monthly_temp_humidity_avg = file_cont.get_average_monthly_data(year, month)
    if monthly_temp_humidity_avg is None:
        print(Constants.IOE)
        exit(1)
    print("Highest Average: {:02d}C"
          .format(monthly_temp_humidity_avg["max_temp_avg"]))
    print("Lowest Average: {:02d}C"
          .format(monthly_temp_humidity_avg["min_temp_avg"]))
    print("Highest Average: {:02d}%"
          .format(monthly_temp_humidity_avg["max_humidity_avg"]))


def get_output_for_e_option(file_cont, date):
    """ This function displays the
    yearly report of highest temperatue,
    lowest temperature and highest humidity
    :param file_cont:
    :param date:
    :return:
    """

    yearly_temp_humidity = file_cont.get_yearly_data(date)
    if yearly_temp_humidity is None:
        print(Constants.IOE)
        exit(1)
    if not yearly_temp_humidity["file_found"]:
        print(Constants.IOE)
        return

    max_temp_date = yearly_temp_humidity["max_temp_year"].split('-')
    min_temp_date = yearly_temp_humidity["min_temp_year"].split('-')
    max_humidity_date = yearly_temp_humidity["max_humidity_year"].split('-')
    print("Highest: {:02d}C on {} {}".format(
        yearly_temp_humidity["max_temp"],
        calendar.month_abbr[int(max_temp_date[1])],
        max_temp_date[2]
    ))
    print("Lowest: {:02d}C on {} {}".format(
        yearly_temp_humidity["min_temp"],
        calendar.month_abbr[int(min_temp_date[1])],
        min_temp_date[2]
    ))
    print("Humid: {:02d}% on {} {}".format(
        yearly_temp_humidity["max_humidity"],
        calendar.month_abbr[int(max_humidity_date[1])],
        max_humidity_date[2]
    ))


def get_output_for_c_option(file_cont, date):
    """ This method displays the bar chart
    representation of hisghest and lowest
    temperatures of the given month of the year
    on separate lines with red + for high
    and blue + for low
    :param file_cont:
    :param date:
    :return:
    """

    date_tokens = date.split("/")
    year = date_tokens[0]
    month_abbr = calendar.month_abbr[int(date_tokens[1])]
    month_name = calendar.month_name[int(date_tokens[1])]
    daily_temps_of_month = file_cont.get_daily_temps_of_month(year, month_abbr)
    if daily_temps_of_month is None:
        print("IO error occured")
        exit(1)
    print(month_name, date_tokens[0])
    i = 1
    while i < len(daily_temps_of_month[0]):
        print("\033[1;30;0m{:02d} ".format(i), end="")
        if daily_temps_of_month[0][i] == Constants.RNF:
            print("\033[1;31;0mmissing")
        else:
            print("\033[1;31;0m+" * int(daily_temps_of_month[0][i]), end="")
            print("\033[1;30;0m {:02d}C".format(daily_temps_of_month[0][i]))
        print("\033[1;30;0m{:02d} ".format(i), end="")
        if daily_temps_of_month[1][i] == Constants.RNF:
            print("\033[1;34;0mmissing")
        else:
            print("\033[1;34;0m+" * int(daily_temps_of_month[1][i]), end="")
            print("\033[1;30;0m {:02d}C".format(daily_temps_of_month[1][i]))
        i += 1


def get_output_for_d_option(file_cont, date):
    """ This method displays the bar chart
    representation of hisghest and lowest
    temperatures of the given month of the year
    on single line with red + for high
    and blue + for low
    :param file_cont:
    :param date:
    :return:
    """

    date_tokens = date.split("/")
    year = date_tokens[0]
    month_abbr = calendar.month_abbr[int(date_tokens[1])]
    month_name = calendar.month_name[int(date_tokens[1])]
    daily_temps_of_month = file_cont.get_daily_temps_of_month(year, month_abbr)
    if daily_temps_of_month is None:
        print("IO error occured")
        exit(1)
    print(month_name, date_tokens[0])
    i = 1
    while i < len(daily_temps_of_month[0]):
        high_temp_miss = (daily_temps_of_month[0][i] == Constants.RNF)
        low_temp_miss = (daily_temps_of_month[1][i] == Constants.RNF)
        print("\033[1;30;0m{:02d} ".format(i), end="")
        if high_temp_miss:
            print("\033[1;31;0mmissing", end="")
        else:
            print("\033[1;31;0m+" * int(daily_temps_of_month[0][i]), end="")
        if low_temp_miss:
            print("\033[1;34;0mmissing", end="")
        else:
            print("\033[1;34;0m+" * int(daily_temps_of_month[1][i]), end="")
        if high_temp_miss:
            print("\033[1;30;0m missing-", end="")
        else:
            print("\033[1;30;0m {:02d}C-"
                  .format(daily_temps_of_month[0][i]), end="")
        if low_temp_miss:
            print("\033[1;30;0mmissing")
        else:
            print("\033[1;30;0m{:02d}C".format(daily_temps_of_month[1][i]))
        i += 1


if __name__ == "__main__":
    __main__()
