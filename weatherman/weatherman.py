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
    TOTAL_ARGUMENTS = len(sys.argv)
    print(TOTAL_ARGUMENTS)

    if TOTAL_ARGUMENTS == 8:
        sepecial_report = {}
        sepecial_report["path"] = sys.argv[1]
        sepecial_report["option1"] = sys.argv[2]
        sepecial_report["date1"] = sys.argv[3]
        sepecial_report["option2"] = sys.argv[4]
        sepecial_report["date2"] = sys.argv[5]
        sepecial_report["option3"] = sys.argv[6]
        sepecial_report["date3"] = sys.argv[7]
        cmd_arg = CmdArg(sepecial_report["option1"], sepecial_report["date1"])
        if cmd_arg.error != "":
            print(cmd_arg.error)
            exit(1)
        cmd_arg = CmdArg(sepecial_report["option2"], sepecial_report["date2"])
        if cmd_arg.error != "":
            print(cmd_arg.error)
            exit(1)
        cmd_arg = CmdArg(sepecial_report["option3"], sepecial_report["date3"])
        if cmd_arg.error != "":
            print(cmd_arg.error)
            exit(1)



    if TOTAL_ARGUMENTS != 4:
        print("Invalid arguments !!!")
        exit(1)

    PATH = sys.argv[1]
    OPTION = sys.argv[2]
    DATE = sys.argv[3]
    CMD_ARGUMENTS = CmdArg(OPTION, DATE)
    CMD_ARGUMENTS.validate_arguments()

    if CMD_ARGUMENTS.error != "":
        print(CMD_ARGUMENTS.error)
        exit(1)

    FILE_CONT = FileContent(PATH)
    if OPTION == '-e':
        YEARLY_TEMP_HUMIDITY = FILE_CONT.get_yearly_data(DATE)
        if YEARLY_TEMP_HUMIDITY is None:
            print("IO error occured")
            exit(1)
        MAX_TEMP_DATE = YEARLY_TEMP_HUMIDITY["max_temp_year"].split('-')
        MIN_TEMP_DATE = YEARLY_TEMP_HUMIDITY["min_temp_year"].split('-')
        MAX_HUMIDITY_DATE = YEARLY_TEMP_HUMIDITY["max_humidity_year"].split('-')
        print("Highest: {:02d}C on {} {}".format(
            YEARLY_TEMP_HUMIDITY["max_temp"],
            calendar.month_abbr[int(MAX_TEMP_DATE[1])],
            MAX_TEMP_DATE[2]
        ))
        print("Lowest: {:02d}C on {} {}".format(
            YEARLY_TEMP_HUMIDITY["min_temp"],
            calendar.month_abbr[int(MIN_TEMP_DATE[1])],
            MIN_TEMP_DATE[2]
        ))
        print("Humid: {:02d}% on {} {}".format(
            YEARLY_TEMP_HUMIDITY["max_humidity"],
            calendar.month_abbr[int(MAX_HUMIDITY_DATE[1])],
            MAX_HUMIDITY_DATE[2]
        ))
    elif OPTION == "-a":
        DATE_TOKENS = DATE.split("/")
        YEAR = DATE_TOKENS[0]
        MONTH = calendar.month_abbr[int(DATE_TOKENS[1])]
        MONTHLY_TEMP_HUMIDITY_AVG = FILE_CONT.get_average_monthly_data(YEAR, MONTH)
        if MONTHLY_TEMP_HUMIDITY_AVG is None:
            print("IO error occured")
            exit(1)
        print("Highest Average: {:02d}C"
              .format(MONTHLY_TEMP_HUMIDITY_AVG["max_temp_avg"]))
        print("Lowest Average: {:02d}C"
              .format(MONTHLY_TEMP_HUMIDITY_AVG["min_temp_avg"]))
        print("Highest Average: {:02d}%"
              .format(MONTHLY_TEMP_HUMIDITY_AVG["max_humidity_avg"]))
    elif OPTION == '-c':
        DATE_TOKENS = DATE.split("/")
        YEAR = DATE_TOKENS[0]
        MONTH = calendar.month_abbr[int(DATE_TOKENS[1])]
        DAILY_TEMPS_OF_MONTH = FILE_CONT.get_daily_temps_of_month(YEAR, MONTH)
        if DAILY_TEMPS_OF_MONTH is None:
            print("IO error occured")
            exit(1)
        i = 1
        while i < len(DAILY_TEMPS_OF_MONTH[0]):
            print("\033[1;30;0m{:02d} ".format(i), end="")
            if DAILY_TEMPS_OF_MONTH[0][i] == Constants.RNF:
                print("\033[1;31;0mmissing")
            else:
                print("\033[1;31;0m+" * int(DAILY_TEMPS_OF_MONTH[0][i]), end="")
                print("\033[1;30;0m {:02d}C".format(DAILY_TEMPS_OF_MONTH[0][i]))
            print("\033[1;30;0m{:02d} ".format(i), end="")
            if DAILY_TEMPS_OF_MONTH[1][i] == Constants.RNF:
                print("\033[1;34;0mmissing")
            else:
                print("\033[1;34;0m+" * int(DAILY_TEMPS_OF_MONTH[1][i]), end="")
                print("\033[1;30;0m {:02d}C".format(DAILY_TEMPS_OF_MONTH[1][i]))
            i += 1
    elif OPTION == '-d':
        DATE_TOKENS = DATE.split("/")
        YEAR = DATE_TOKENS[0]
        MONTH = calendar.month_abbr[int(DATE_TOKENS[1])]
        DAILY_TEMPS_OF_MONTH = FILE_CONT.get_daily_temps_of_month(YEAR, MONTH)
        if DAILY_TEMPS_OF_MONTH is None:
            print("IO error occured")
            exit(1)
        i = 1
        while i < len(DAILY_TEMPS_OF_MONTH[0]):
            HIGH_TEMP_MISS = (DAILY_TEMPS_OF_MONTH[0][i] == Constants.RNF)
            LOW_TEMP_MISS = (DAILY_TEMPS_OF_MONTH[1][i] == Constants.RNF)
            print("\033[1;30;0m{:02d} ".format(i), end="")
            if HIGH_TEMP_MISS:
                print("\033[1;31;0mmissing", end="")
            else:
                print("\033[1;31;0m+" * int(DAILY_TEMPS_OF_MONTH[0][i]), end="")
            if LOW_TEMP_MISS:
                print("\033[1;34;0mmissing", end="")
            else:
                print("\033[1;34;0m+" * int(DAILY_TEMPS_OF_MONTH[1][i]), end="")
            if HIGH_TEMP_MISS:
                print("\033[1;30;0m missing-", end="")
            else:
                print("\033[1;30;0m {:02d}C-"
                      .format(DAILY_TEMPS_OF_MONTH[0][i]), end="")
            if LOW_TEMP_MISS:
                print("\033[1;30;0mmissing")
            else:
                print("\033[1;30;0m{:02d}C".format(DAILY_TEMPS_OF_MONTH[1][i]))
            i += 1




if __name__ == "__main__":
    __main__()
