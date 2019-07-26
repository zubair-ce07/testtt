#!/usr/bin/python3
import os
import argparse

from data_reader import *
from reports import *
from result_calculator import *


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        msg = "Invalid directory: '{0}'.".format(string)
        raise argparse.ArgumentTypeError(msg)

def valid_year(s):
    try:
        date = datetime.strptime(s, "%Y")
        if date.year < 2004 or date.year > 2016:
            msg = "Valid years: 2004 - 2016"
            raise argparse.ArgumentTypeError(msg)
        return s
    except ValueError:
        msg = "Invalid year: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def valid_date_format(s):
    try:
        date_entered = datetime.strptime(s,"%Y/%m")
        starting_date = datetime.strptime("2004/2","%Y/%m")
        ending_date = datetime.strptime("2016/10","%Y/%m")
        if not (starting_date < date_entered and date_entered < ending_date):
            msg = "Valid date: 2004/3 - 2016/9"
            raise argparse.ArgumentTypeError(msg)
        return s
    except Exception as e:
        msg = "invalid date/format: '{0}'.".format(s) + " Plase use yyyy/mm"
        raise argparse.ArgumentTypeError(msg)

def setup_arguments():

    parser = argparse.ArgumentParser(description='Weatherman, Weather data analyser tool.')
    parser.add_argument('data_directory', type=dir_path,
                        help='Weather data directory path')
    parser.add_argument('-e', type=valid_year)
    parser.add_argument('-a', type=valid_date_format)
    parser.add_argument('-c', type=valid_date_format)


    return (parser.parse_args())

def perform_monthly_operations(command, command_argument, reader, reports, processor):
    given_year = command_argument.split("/")[0]
    month_number = command_argument.split("/")[1]

    monthly_records = reader.parse_weather_records(given_year = given_year,month_number = month_number)
    processor.monthly_records = monthly_records

    if (command == 'a'):
        result = processor.get_monthly_avg_results()
        reports.print_average_report(result, month_number, given_year)
    elif (command == 'c'):
        reports.print_monthly_report(monthly_records, month_number, given_year)

def main():
    args = setup_arguments()
    path = args.data_directory
    reader = WeathermanFileReader(path)
    reports = WeathermanReportPrinter()
    processor = ResultCalculator()

    if (args.e):
        given_year = args.e
        yearly_records = []
        for month_number in range(1,13):
            monthly_records = reader.parse_weather_records(given_year = given_year,month_number = month_number)
            if (monthly_records):
                yearly_records.append(monthly_records)

        processor.yearly_records = yearly_records
        reports.print_yearly_report(processor.get_yearly_temperature_peaks())

    if (args.a):
        perform_monthly_operations('a', args.a, reader, reports, processor)

    if (args.c):
        perform_monthly_operations('c', args.c, reader, reports, processor)

if __name__ == "__main__":

    main()
