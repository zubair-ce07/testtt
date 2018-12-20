from datetime import datetime
import argparse
import os

from parser import DataParser
from calculation import Calculations
from report import Report
import colors


def valid_directory(path):
    try:
        if os.path.isdir(path):
            return path
        else:
            raise ValueError(f"{colors.RED}Invalid Directory ({colors.RESET}{path}{colors.RED}){colors.RESET}")
    except ValueError as error:
        print(error)


def valid_month(month_date):
    try:
        return datetime.strptime(month_date, '%Y')
    except ValueError:
        pass
    try:
        return datetime.strptime(month_date, '%Y/%m')
    except ValueError:
        print(f"{colors.RED}Invalid date {colors.RESET}")


def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('path', type=valid_directory, help='Enter path of the directory!')
    args_parser.add_argument('-e', type=valid_month)
    args_parser.add_argument('-a', type=valid_month)
    args_parser.add_argument('-c', type=valid_month)
    args_parser.add_argument('-d', type=valid_month)
    args = args_parser.parse_args()

    data_parser = DataParser()
    calculator = Calculations()
    report_generator = Report()

    if args.e:
        files_record = data_parser.weather_record(args.e.year, args.path)
        year_weather_data = data_parser.read_weather_data(files_record)
        calculated_data = calculator.year_peak_calculation(year_weather_data)
        report_generator.year_peak_report(calculated_data)

    if args.a:
        files_record = data_parser.weather_record(args.a.year, args.path, args.a.month)
        month_weather_data = data_parser.read_weather_data(files_record)
        calculated_data = calculator.month_average_calculation(month_weather_data)
        report_generator.month_average_report(calculated_data)

    if args.c:
        files_record = data_parser.weather_record(args.c.year, args.path, args.c.month)
        month_weather_data = data_parser.read_weather_data(files_record)
        calculated_data = calculator.month_peak_calculation(month_weather_data)
        report_generator.bar_chart_report(calculated_data)

    if args.d:
        files_record = data_parser.weather_record(args.d.year, args.path, args.d.month)
        month_weather_data = data_parser.read_weather_data(files_record)
        calculated_data = calculator.month_peak_calculation(month_weather_data)
        report_generator.bar_chart_report_bonus(calculated_data)


if __name__ == '__main__':
    main()
