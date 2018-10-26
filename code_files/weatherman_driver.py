#!/usr/bin/python3.6


import argparse
import os
import glob
import datetime

import constants
from weather_data_analysis import WeatherDataAnalysis
from weather_readings import WeatherReadings
from weather_reporting import WeatherReporting
from csv_file_data_holder import CsvFileDataHolder


def parse_records(operation, dates, weather_records, path_to_files):
    if not dates:
        return

    for date in dates:
        analyse_weather = WeatherDataAnalysis()
        report_weather = WeatherReporting()
        current_year = date
        month_number = 0
        record_info = current_year
        if operation != 'e':
            current_year = date.split('/')[0]
            month_number = int(date.split('/')[1])-1
            record_info = (
                constants.MONTHS_NAME[month_number] + ', ' + current_year)
        add_current_year_weather_readings(
            current_year, weather_records, path_to_files)
        report = analyse_weather.analyse(
            operation, weather_records, current_year, month_number)
        report_weather.display_report(report, operation, record_info)


def add_current_year_weather_readings(current_year, weather_records, path_to_files):
    months_in_year = weather_records.get_months_data_of_year(
        current_year)
    if months_in_year is None:
        months_in_year = []
        for name in constants.MONTHS_NAME:
            current_month = name[:3]
            weather_report_file_path = glob.glob(
                path_to_files+'/*_weather_'+current_year+'_'+current_month+'.txt')
            if weather_report_file_path:
                month = CsvFileDataHolder()
                month.read_csv_file(weather_report_file_path.pop())
                months_in_year.append(month)
            else:
                months_in_year.append(None)
        weather_records.add_new_year(current_year, months_in_year)


def year_validator(date_value):
    try:
        datetime.datetime.strptime(date_value, '%Y')
        return date_value
    except ValueError:
        raise argparse.ArgumentTypeError(constants.YEAR_ARGUMENT_ERROR_MESSAGE)


def year_and_month_validator(date_value):
    try:
        datetime.datetime.strptime(date_value, '%Y/%m')
        return date_value
    except ValueError:
        raise argparse.ArgumentTypeError(
            constants.MONTH_ARGUMENT_ERROR_MESSAGE)


def path_validator(path_value):
    if os.access(path_value, os.R_OK):
        return path_value
    else:
        raise argparse.ArgumentTypeError(constants.DIRECTORY_ERROR_MESSAGE)


def driver():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=path_validator,
                        help=constants.PATH_ARGUMENT_DISCRIPTION)
    parser.add_argument('-e', type=year_validator, nargs='+',
                        help=constants.YEAR_ARGUMENT_DISCRIPTION)
    parser.add_argument('-a', type=year_and_month_validator,
                        nargs='+', help=constants.MONTH_ARGUMENT_DISCRIPTION)
    parser.add_argument('-c', type=year_and_month_validator, nargs='+',
                        help=constants.MONTH_BARCHART_ARGUMENT_DISCRIPTION)
    args = parser.parse_args()
    weather_records = WeatherReadings()
    parse_records('e', args.e, weather_records, args.path)
    parse_records('a', args.a, weather_records, args.path)
    parse_records('c', args.c, weather_records, args.path)


if __name__ == '__main__':
    driver()
