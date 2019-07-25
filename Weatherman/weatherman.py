#!/usr/bin/python3
import os
import argparse

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

def setup_arguments():

    parser = argparse.ArgumentParser(description='Weatherman, Weather data analyser tool.')
    parser.add_argument('data directory', type=dir_path,
                        help='Weather data directory path')
    parser.add_argument('-e', type=valid_year)
    parser.add_argument('-a', type=valid_date_format)
    parser.add_argument('-c', type=valid_date_format)


    return vars(parser.parse_args())

def perform_monthly_operations(command, command_argument, reader, reports, processor):
    given_year = command_argument.split("/")[0]
    month_number = command_argument.split("/")[1]

    monthly_records = reader.get_monthly_data(given_year = given_year,month_number = month_number)
    processor.monthly_records = monthly_records

    if (command == 'a'):
        result = processor.get_monthly_avg_results()
        reports.print_average_report(result, month_number, given_year)
    elif (command == 'c'):
        reports.print_monthly_report(monthly_records, month_number, given_year)

def main():
    args = setup_arguments()
    path = args['data directory']
    reader = WeathermanFileReader(path)
    reports = WeathermanReportPrinter()
    processor = FactsCalculation()

    if (args['e']):
        command = 'e'
        given_year = str(args['e'])
        yearly_records = []
        for month_number in range(1,13):
            monthly_records = reader.get_monthly_data(given_year = given_year,month_number = month_number)
            if (monthly_records):
                yearly_records.append(monthly_records)

        processor.yearly_records = yearly_records
        reports.print_yearly_report(processor.get_yearly_temperature_peaks())

    if (args['a']):
        perform_monthly_operations('a', str(args['a']), reader, reports, processor)

    if (args['c']):
        perform_monthly_operations('c', str(args['c']), reader, reports, processor)

if __name__ == "__main__":

    main()
