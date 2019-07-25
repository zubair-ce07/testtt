import argparse
import os

from datetime import datetime

from weather_parser import FileParser
from weather_calculations import WeatherCalculations
from weather_reporter import ReportGenerator


def is_valid_year(year):
    if int(year) > 2016:
        raise argparse.ArgumentTypeError(f"Max year is 2016")
    return int(year)


def is_valid_year_month(date):
    try:
        date = datetime.strptime(date, '%Y/%m')
    except Exception:
        raise argparse.ArgumentTypeError(f"Invalid Date")

    return is_valid_year(date.year), int(date.month)


def is_valid_path(file_path):
    if os.path.isdir(file_path):
        return file_path
    raise argparse.ArgumentTypeError(f"Invalid Directory")


def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="The local file path of weather files", type=is_valid_path)
    parser.add_argument("-e", help="highest, lowest, highest humidity for a given year", type=is_valid_year)
    parser.add_argument("-a", help="average highest, lowest, mean humidity for a given month", type=is_valid_year_month)
    parser.add_argument("-c", help="separate bar charts for highest and lowest temp", type=is_valid_year_month)
    parser.add_argument("-b", help="single bar chart for highest and lowest temp", type=is_valid_year_month)

    return parser.parse_args()


if __name__ == "__main__":
    args = check_args()
    file_path = args.file_path
    parsed_records = FileParser().file_reader(file_path)
    report_gen = ReportGenerator()
    calculations = WeatherCalculations()

    if args.e:
        weather_result = calculations.get_weather_results(parsed_records, args.e)
        report_gen.print_yearly(weather_result)

    if args.a:
        year, month = args.a
        weather_result = calculations.get_weather_results(parsed_records, year, month)
        report_gen.print_monthly(weather_result)

    if args.c:
        year, month = args.c
        weather_result = calculations.get_weather_results(parsed_records, year, month)
        report_gen.print_double_chart(weather_result)

    if args.b:
        year, month = args.b
        weather_result = calculations.get_weather_results(parsed_records, year, month)
        report_gen.print_bonus_chart(weather_result)
