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


def parse_records(operation, date_values, complete_weather_records, weather_records_files_path):
    if not date_values:
        return
    for date in date_values:
        analyse_weather = WeatherDataAnalysis()
        report_weather = WeatherReporting()
        current_year = date
        record_info = current_year
        month_number = 0
        if operation is not 'e':
            current_year = date.split('/')[0]
            month_number = int(date.split('/')[1])-1
            record_info = (
                constants.MONTHS_NAME[month_number] + ', ' + current_year)
        add_current_year_weather_readings(
            current_year, complete_weather_records, weather_records_files_path)
        report = analyse_weather.analyse(
            operation, complete_weather_records, current_year, month_number)
        report_weather.display_report(report, operation, record_info)


def add_current_year_weather_readings(current_year, complete_weather_records, weather_records_files_path):
    months_in_year = complete_weather_records.get_months_data_of_year(
        current_year)
    if months_in_year is None:
        months_in_year = []
        for name in constants.MONTHS_NAME:
            current_month = name[:3]
            weather_report_file_path = glob.glob(
                weather_records_files_path+'/*_weather_'+current_year+'_'+current_month+'.txt')
            if weather_report_file_path:
                month = CsvFileDataHolder()
                month.read_csv_file(weather_report_file_path.pop())
                months_in_year.append(month)
            else:
                months_in_year.append(None)
        complete_weather_records.add_new_year(current_year, months_in_year)


def year_validator(date_value):
    try:
        datetime.datetime.strptime(date_value, '%Y')
        return date_value
    except ValueError:
        print(constants.YEAR_ARGUMENT_ERROR_MESSAGE)
        raise argparse.ArgumentTypeError


def year_and_month_validator(date_value):
    try:
        datetime.datetime.strptime(date_value, '%Y/%m')
        return date_value
    except ValueError:
        print(constants.MONTH_ARGUMENT_ERROR_MESSAGE)
        raise argparse.ArgumentTypeError


def driver():
    parser = argparse.ArgumentParser()
    try:
        parser.add_argument('path', help=constants.PATH_ARGUMENT_DISCRIPTION)
        parser.add_argument('-e', type=year_validator, nargs='*',
                            help=constants.YEAR_ARGUMENT_DISCRIPTION)
        parser.add_argument('-a', type=year_and_month_validator,
                            nargs='*', help=constants.MONTH_ARGUMENT_DISCRIPTION)
        parser.add_argument('-c', type=year_and_month_validator, nargs='*',
                            help=constants.MONTH_BARCHART_ARGUMENT_DISCRIPTION)
        args = parser.parse_args()
        if os.access(args.path, os.R_OK):
            complete_weather_records = WeatherReadings()
            parse_records('e', args.e, complete_weather_records, args.path)
            parse_records('a', args.a, complete_weather_records, args.path)
            parse_records('c', args.c, complete_weather_records, args.path)
        else:
            print(constants.DIRECTORY_ERROR_MESSAGE)
    except argparse.ArgumentTypeError:
        pass


if __name__ == '__main__':
    driver()
