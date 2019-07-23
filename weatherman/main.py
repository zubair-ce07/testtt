import argparse
import os
from datetime import datetime

from calculations import WeatherCalculator
from parser import Parser
from reporter import Reports


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="data_path", type=lambda p: p if os.path.exists(p) else parser.error("Invalid Path"))
    parser.add_argument('-e', action='store', dest='year_to_report',  type=lambda d: datetime.strptime(d, "%Y").year,
                        help="Enter Year to report. e.g. 2004")
    parser.add_argument('-a', action='store', dest='month_to_report', type=lambda d: datetime.strptime(d, "%Y/%m"),
                        help="Enter year and month number. e.g. 2004/6")
    parser.add_argument('-c', action='store', dest='month_to_plot', type=lambda d: datetime.strptime(d, "%Y/%m"),
                        help="Enter year and month number. e.g. 2004/6")
    return parser.parse_args()


def main():
    args = parse_args()
    reports = Reports()

    if args.year_to_report:
        records = Parser(args.data_path, args.year_to_report).read_files()
        calculations = WeatherCalculator(records).calculate_weather()
        print('\n')
        reports.report_year(calculations)
        print('\n')

    if args.month_to_report:
        year, month = args.month_to_report.year, args.month_to_report.month
        records = Parser(args.data_path, year, month).read_files()
        calculations = WeatherCalculator(records).calculate_weather()
        print('\n')
        reports.report_month(calculations)
        print('\n')

    if args.month_to_plot:
        year, month = args.month_to_plot.year, args.month_to_plot.month
        records = Parser(args.data_path, year, month).read_files()
        print('\n')
        reports.plot_month(records)
        print('\n')
        reports.plot_month_horizontal(records)
        print('\n')


if __name__ == "__main__":
    main()
