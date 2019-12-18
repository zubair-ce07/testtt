import argparse
import os
import re
from datetime import datetime

from constants import ReportTypes
from report_generator import ReportGenerator
from weather_data_analyzer import WeatherDataAnalyzer
from weather_data_parser import WeatherDataParser


def main():
    user_args = initialize_arguments()

    parser = WeatherDataParser(user_args.dir_path)
    parser.load_data_from_files()
    weather_records = parser.fetch_records()

    if user_args.e:
        show_extreme_stats(weather_records, user_args.e)

    if user_args.a:
        show_mean_stats(weather_records, user_args.a.month, user_args.a.year)

    if user_args.c:
        show_graphs(weather_records, user_args.c.month, user_args.c.year)


def show_extreme_stats(weather_records, year):
    results = WeatherDataAnalyzer(weather_records, year=year).calculate_extremes()

    generate_report(results, ReportTypes.SHOW_EXTREMES)


def show_mean_stats(weather_records, month, year):
    results = WeatherDataAnalyzer(weather_records, month=month, year=year).calculate_averages()

    generate_report(results, ReportTypes.SHOW_MEANS)


def show_graphs(weather_records, month, year):
    results = WeatherDataAnalyzer(weather_records).fetch_records_of_month(month, year)

    generate_report(results, ReportTypes.SHOW_GRAPHS)


def generate_report(calculations_result, report_type):
    report_generator = ReportGenerator(calculations_result)
    report_generator.generate(report_type)


def initialize_arguments():
    description = 'A weather report generator which shows different reports based upon user arguments'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('dir_path',
                        type=lambda path: path
                        if os.path.isdir(path)
                        else parser.error(f'{path} is not a valid path'),
                        help='Path to the directory of data files')

    parser.add_argument('-e',
                        type=lambda year_string: int(year_string)
                        if re.match(r'^\d{1,4}$', year_string)
                        else parser.error(f'Not a valid year: {year_string}. Acceptable format is YYYY'),
                        help='Displays extreme stats in a year')
    parser.add_argument('-a',
                        type=lambda date_string: datetime.strptime(date_string, '%Y/%m')
                        if re.match(r'^\d{1,4}/\d{1,2}$', date_string)
                        else parser.error(f'Not a valid date: {date_string}. Acceptable format is YYYY/MM'),
                        help="Displays average stats in a year's month")

    parser.add_argument('-c',
                        type=lambda date_string: datetime.strptime(date_string, '%Y/%m')
                        if re.match(r'^\d{1,4}/\d{1,2}$', date_string)
                        else parser.error(f'Not a valid date: {date_string}. Acceptable format is YYYY/MM'),
                        help="Displays graphs of every day temperature in a year's month")

    return parser.parse_args()


if __name__ == '__main__':
    main()
