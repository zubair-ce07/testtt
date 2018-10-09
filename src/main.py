#!/usr/bin/python3
import argparse
from datetime import datetime

import report_generator
from calculations import WeatherCalculations


def make_month_date(date):
    return datetime.strptime(date, '%Y/%m')


def make_year_date(date):
    return datetime.strptime(date, '%Y')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", type=str)
    parser.add_argument('-e', type=make_year_date, nargs='*')
    parser.add_argument('-a', type=make_month_date, nargs='*')
    parser.add_argument('-c', type=make_month_date, nargs='*')
    args = parser.parse_args()

    data_calculations = WeatherCalculations()
    all_data = data_calculations.all_weather_record(args.dir_path)

    output_writer = report_generator.OutputGenerator()

    if args.e:
        for date in args.e:
            output_writer.print_extreme_record(
                data_calculations.year_record(all_data, date))
    if args.a:
        for date in args.a:
            output_writer.print_average_record(
                data_calculations.month_record(all_data, date))
    if args.c:
        for date in args.c:
            output_writer.print_temp_chart_bounus(
                data_calculations.month_record(all_data, date))


if __name__ == '__main__':
    main()
