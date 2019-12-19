import argparse
import os
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
        results = WeatherDataAnalyzer(weather_records, date=user_args.e).calculate_extremes()
        generate_report(results, ReportTypes.SHOW_EXTREMES)

    if user_args.a:
        results = WeatherDataAnalyzer(weather_records, date=user_args.a).calculate_averages()
        generate_report(results, ReportTypes.SHOW_MEANS)

    if user_args.c:
        results = WeatherDataAnalyzer(weather_records).fetch_records_of_month(user_args.c)
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
                        type=lambda year: datetime.strptime(year, '%Y'),
                        help='Displays extreme stats in a year')
    parser.add_argument('-a',
                        type=lambda date: datetime.strptime(date, '%Y/%m'),
                        help="Displays average stats in a year's month")

    parser.add_argument('-c',
                        type=lambda date: datetime.strptime(date, '%Y/%m'),
                        help="Displays graphs of every day temperature in a year's month")

    return parser.parse_args()


if __name__ == '__main__':
    main()
