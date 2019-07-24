#!/usr/bin/python3
import os
import argparse

from errors import *
from data_reader import *
from reports import *


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        msg = "Invalid directory: '{0}'.".format(string)
        raise argparse.ArgumentTypeError(msg)

def valid_year(s):
    try:
        datetime.strptime(s, "%Y")
        return s
    except ValueError:
        msg = "Invalid year: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def valid_date_format(s):
    try:
        datetime.strptime(s,"%Y/%m")
        return s
    except Exception as e:
        msg = "invalid date/format: '{0}'.".format(s) + " Plase use yyyy/mm"
        raise argparse.ArgumentTypeError(msg)

def add_argument_details():

    parser = argparse.ArgumentParser(description='Weatherman, Weather data analyser tool.')
    parser.add_argument('data directory', type=dir_path,
                        help='Weather data directory path')


    #group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-e', type=valid_year)
    parser.add_argument('-a', type=valid_date_format)
    parser.add_argument('-c', type=valid_date_format)


    return vars(parser.parse_args())


def main():

    args = add_argument_details()

    path = args['data directory']
    reader = WeathermanFileReader(path)
    reports = WeathermanReportPrinter()

    for arg in args:
        if (args[arg] and (arg in ['a','c','e'])):
            command = arg
            command_argument = str(args[arg])
            if (command == 'e'):
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


            elif (command == 'a'):
                given_year = command_argument.split("/")[0]
                month_number = command_argument.split("/")[1]

                avg_facts = reader.get_monthly_data(given_year = given_year,month_number = month_number,selected_fields = average_temperature_fields\
                                                ,command = command)
                reports.print_average_report(avg_facts, month_number, given_year)


            elif (command == 'c'):
                given_year = command_argument.split("/")[0]
                month_number = command_argument.split("/")[1]

                monthlyRecords = reader.get_monthly_data(given_year = given_year,month_number = month_number,selected_fields = temperature_fields\
                                                ,command = command)
                reports.print_monthly_report(monthlyRecords, month_number, given_year)




if __name__ == "__main__":
    try:
        main()
    except InvalidArguments as error:
        print(error.message)
    except:
        print("Something went wrong")
