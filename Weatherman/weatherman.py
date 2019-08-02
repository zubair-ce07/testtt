#!/usr/bin/python3
import os
from datetime import datetime
import argparse

from data_reader import WeathermanFileReader
from reports import WeathermanReportPrinter
from result_calculator import WeatherAnalyzer


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
        return date
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
        return date_entered
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

def perform_monthly_operations(command, date, weather_data_reader, report_printer, weather_analyzer):
    monthly_weather_records = weather_data_reader.get_weather_records(
        year=date.year,
        month=date.month
    )
    if command == 'a':
        weather_analyzer.weather_records = monthly_weather_records
        result = weather_analyzer.get_monthly_avg_results()
        report_printer.print_average_report(result)
    elif command == 'c':
        report_printer.print_monthly_report(monthly_weather_records, date.month, date.year)

def main():
    commandline_arguments = setup_arguments()
    weather_data_directory_path = commandline_arguments.data_directory
    weather_data_reader = WeathermanFileReader(weather_data_directory_path)
    weather_data_reader.read_all_data()
    report_printer = WeathermanReportPrinter()
    weather_analyzer = WeatherAnalyzer(weather_records=[])

    if commandline_arguments.e:
        given_year = commandline_arguments.e.year
        yearly_weather_records = []
        yearly_weather_records = weather_data_reader.get_weather_records(year=given_year)

        weather_analyzer.weather_records = yearly_weather_records
        report_printer.print_yearly_report(weather_analyzer.get_yearly_temperature_peaks())

    if commandline_arguments.a:
        perform_monthly_operations('a', commandline_arguments.a, \
            weather_data_reader, report_printer, weather_analyzer)

    if commandline_arguments.c:
        perform_monthly_operations('c', commandline_arguments.c, \
            weather_data_reader, report_printer, weather_analyzer)

if __name__ == "__main__":

    main()
