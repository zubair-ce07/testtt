from datetime import datetime
import argparse
import os

from parser import DataParser
from calculation import Calculations
from report import Report
import color


def valid_path(path):
    try:
        if os.path.isdir(path):
            return path
        else:
            raise ValueError(f"{color.RED}Invalid Directory ({color.RESET}{path}{color.RED}){color.RESET}")
    except ValueError as error:
        print(error)


def valid_date(month_date):
    try:
        return datetime.strptime(month_date, '%Y')
    except ValueError:
        pass
    try:
        return datetime.strptime(month_date, '%Y/%m')
    except ValueError:
        print(f"{color.RED}Invalid date {color.RESET}")


def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('path', type=valid_path, help='Enter path of the directory!')
    args_parser.add_argument('-e', type=valid_date)
    args_parser.add_argument('-a', type=valid_date)
    args_parser.add_argument('-c', type=valid_date)
    args_parser.add_argument('-d', type=valid_date)
    args = args_parser.parse_args()

    data_parser = DataParser()
    calculator = Calculations()
    report_generator = Report()

    if args.e:
        files_record = data_parser.find_record(args.e.year, args.path)
        year_weather_data = data_parser.read_weather_data(files_record)
        calculated_data = calculator.calculate_peak_values(year_weather_data)
        report_generator.generate_peak_values(calculated_data)

    if args.a:
        files_record = data_parser.find_record(args.a.year, args.path, args.a.month)
        month_weather_data = data_parser.read_weather_data(files_record)
        calculated_data = calculator.calculate_average_values(month_weather_data)
        report_generator.generate_peak_values(calculated_data, args.a.month)

    if args.c:
        files_record = data_parser.find_record(args.c.year, args.path, args.c.month)
        month_weather_data = data_parser.read_weather_data(files_record)
        calculated_data = calculator.calculate_peak_values(month_weather_data, args.c.month)
        report_generator.generate_bar_chart(calculated_data)

    if args.d:
        files_record = data_parser.find_record(args.d.year, args.path, args.d.month)
        month_weather_data = data_parser.read_weather_data(files_record)
        calculated_data = calculator.calculate_peak_values(month_weather_data, args.d.month)
        report_generator.generate_bar_chart(calculated_data, args.d.month)


if __name__ == '__main__':
    main()
