#!/usr/bin/python3
import os
import argparse

from errors import *
from data_reader import *
from reports import *
from info_extraction import *


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
    processor = FactsCalculation()

    for arg in args:
        if (args[arg] and (arg in ['a','c','e'])):
            command = arg
            command_argument = str(args[arg])
            if (command == 'e'):
                given_year = command_argument

                yearly_records = []
                for month_number in range(1,13):
                    monthly_records = reader.get_monthly_data(given_year = given_year,month_number = month_number)
                    if (monthly_records):
                        yearly_records.append(monthly_records)

                processor.yearly_records = yearly_records
                reports.print_yearly_report(processor.get_yearly_temperature_peaks())

            elif (command == 'a' or command == 'c'):
                given_year = command_argument.split("/")[0]
                month_number = command_argument.split("/")[1]

                monthly_records = reader.get_monthly_data(given_year = given_year,month_number = month_number)
                processor.monthly_records = monthly_records

                if (command == 'a'):
                    result = processor.get_monthly_avg_results()
                    reports.print_average_report(result, month_number, given_year)
                elif (command == 'c'):
                    reports.print_monthly_report(monthly_records, month_number, given_year)


if __name__ == "__main__":
    try:
        main()
    except InvalidArguments as error:
        print(error.message)
    except:
        print("Something went wrong")
