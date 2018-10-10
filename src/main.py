#!/usr/bin/python3
import argparse
from datetime import datetime

from calculations import WeatherCalculations
from report_generator import ReportGenerator


def month_date(date):
    return datetime.strptime(date, '%Y/%m')


def year_date(date):
    return datetime.strptime(date, '%Y')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", type=str)
    parser.add_argument('-e', type=year_date, nargs='*')
    parser.add_argument('-a', type=month_date, nargs='*')
    parser.add_argument('-c', type=month_date, nargs='*')
    args = parser.parse_args()

    data_calculations = WeatherCalculations()
    data = data_calculations.all_weather_record(args.dir_path)

    report_generator = ReportGenerator()

    if args.e:
        for date in args.e:
            report_generator.print_extreme_record(data_calculations.year_records(data, date))
    if args.a:
        for date in args.a:
            report_generator.print_average_record(data_calculations.month_records(data, date))
    if args.c:
        for date in args.c:
            report_generator.print_temp_chart_bounus(data_calculations.month_records(data, date))


if __name__ == '__main__':
    main()
