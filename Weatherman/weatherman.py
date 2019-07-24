#!/usr/bin/python3
import sys
import os

from errors import *
from data_reader import *
from reports import *


def validate_arguments(args):
    if (len(args) < 2) or (len(args) % 2 == 1):
        raise InvalidArguments("Invalid arguments")

    path = args[1];
    if (not os.path.isdir(path)):
        raise InvalidArguments("Given folder does not exist");
    return path


def main():

    path = validate_arguments(sys.argv)
    reader = WeathermanFileReader(path)
    reports = WeathermanReportPrinter()

    argIndex = 2

    for arg in range(2, len(sys.argv), 2):
        command = sys.argv[argIndex]
        command_argument = sys.argv[argIndex + 1]
        if (command == '-e'):
            given_year = command_argument

            highest_temp = {}
            min_temp = {}
            max_humidity = {}
            for month_number in range(1,13):

                facts = reader.get_monthly_data(given_year = given_year,month_number = month_number,selected_fields = yearly_record_fields,\
                                                command = command,highest_temp = highest_temp, min_temp = min_temp, max_humidity = max_humidity)
                highest_temp = facts[0]
                min_temp = facts[1]
                max_humidity = facts[2]
            reports.print_yearly_report(facts)


        elif (command == '-a'):
            given_year = command_argument.split("/")[0]
            month_number = command_argument.split("/")[1]

            avg_facts = reader.get_monthly_data(given_year = given_year,month_number = month_number,selected_fields = average_temperature_fields\
                                            ,command = command)
            reports.print_average_report(avg_facts, month_number, given_year)


        elif (command == '-c'):
            given_year = command_argument.split("/")[0]
            month_number = command_argument.split("/")[1]

            monthlyRecords = reader.get_monthly_data(given_year = given_year,month_number = month_number,selected_fields = temperature_fields\
                                            ,command = command)
            reports.print_monthly_report(monthlyRecords, month_number, given_year)

        else:
            raise InvalidArguments("Invalid command: " + command);

        argIndex += 2;


if __name__ == "__main__":
    try:
        main()
    except InvalidArguments as error:
        print(error.message)
    '''except:
        print("Something went wrong")'''
