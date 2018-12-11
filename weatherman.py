import argparse
import os
import datareader
import reports
import reportgenerator
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument('-path', type=dir_path)
    parser.add_argument('-e', '--yearly', nargs = '*', help='yearly report', type=date_year, required=False, default='')
    parser.add_argument('-a', '--monthly', help='monthly report', type=date_month, required=False, default='')
    parser.add_argument('-c', '--bar_chart', help='bar chart report', type=date_month, required=False, default='')

    return parser.parse_args()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def date_year(date):
    if date:
        try:
            return datetime.strptime(date, '%Y')
        except ValueError:
            raise argparse.ArgumentTypeError(f"Given Date({date}) not valid")


def date_month(date):
    if date:
        try:
            return datetime.strptime(date, '%Y/%m')
        except ValueError:
            raise argparse.ArgumentTypeError(f"Given Date({date}) not valid")


def main():
    parsed_args = parse_arguments()
    weather_records = datareader.data_parser(parsed_args.path)

    if parsed_args.yearly:

        for year in parsed_args.yearly:
            year_weather_record = reports.yearly_report(weather_records, year)
            reportgenerator.generate_yearly_report(year_weather_record)

    if parsed_args.monthly:
        month_weather_record = reports.monthly_report(weather_records, parsed_args.monthly)
        reportgenerator.generate_monthly_report(month_weather_record)

    if parsed_args.bar_chart:
        bar_chart_record = reports.bar_chart_report(weather_records, parsed_args.bar_chart)
        reportgenerator.generate_bonus_bar_chart(bar_chart_record)


if __name__ == "__main__":
    main()
