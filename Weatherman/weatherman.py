#!/usr/bin/python3
import os
from datetime import datetime
import argparse

from data_reader import WeathermanFileReader
from reports import WeathermanReportPrinter
from result_calculator import ResultCalculator


def dir_path(string):
    if os.path.isdir(string):
        return string
    msg = "Invalid directory: '{0}'.".format(string)
    raise argparse.ArgumentTypeError(msg)

def valid_year(argument_value):
    try:
        date = datetime.strptime(argument_value, "%Y")
        if date.year < 2004 or date.year > 2016:
            msg = "Valid years: 2004 - 2016"
            raise argparse.ArgumentTypeError(msg)
        return argument_value
    except ValueError:
        msg = "Invalid year: '{0}'.".format(argument_value)
        raise argparse.ArgumentTypeError(msg)

def valid_date_format(argument_value):
    try:
        date_entered = datetime.strptime(argument_value, "%Y/%m")
        starting_date = datetime.strptime("2004/7", "%Y/%m")
        ending_date = datetime.strptime("2016/9", "%Y/%m")
        if (starting_date > date_entered) or (date_entered > ending_date):
            raise argparse.ArgumentTypeError()
        return argument_value
    except Exception:
        msg = "invalid date/format: '{0}'.".format(argument_value) + \
                " Plase use format: yyyy/mm and valid date: 2004/7 - 2016/9"
        raise argparse.ArgumentTypeError(msg)

def setup_arguments():
    parser = argparse.ArgumentParser(description='Weatherman, Weather data analyser tool.')
    parser.add_argument('data_directory', type=dir_path,
                        help='Weather data directory path')
    parser.add_argument('-e', type=valid_year)
    parser.add_argument('-a', type=valid_date_format)
    parser.add_argument('-c', type=valid_date_format)


    return parser.parse_args()

def perform_monthly_operations(command, command_argument, reader, reports, processor):
    given_year = command_argument.split("/")[0]
    month_number = command_argument.split("/")[1]

    monthly_weather_records = reader.parse_weather_records(given_year=given_year, \
                                            month_number=month_number)
    processor.monthly_weather_records = monthly_weather_records

    if command == 'a':
        result = processor.get_monthly_avg_results()
        reports.print_average_report(result)
    elif command == 'c':
        reports.print_monthly_report(monthly_weather_records, month_number, given_year)

def main():
    args = setup_arguments()
    path = args.data_directory
    reader = WeathermanFileReader(path)
    reports = WeathermanReportPrinter()
    processor = ResultCalculator(monthly_weather_records=[], yearly_weather_records=[])

    if args.e:
        given_year = args.e
        yearly_weather_records = []
        for month_number in range(1, 13):
            monthly_weather_records = reader.parse_weather_records(given_year=given_year, \
                                            month_number=month_number)
            if monthly_weather_records:
                yearly_weather_records.append(monthly_weather_records)

        processor.yearly_weather_records = yearly_weather_records
        reports.print_yearly_report(processor.get_yearly_temperature_peaks())

    if args.a:
        perform_monthly_operations('a', args.a, reader, reports, processor)

    if args.c:
        perform_monthly_operations('c', args.c, reader, reports, processor)

if __name__ == "__main__":

    main()
