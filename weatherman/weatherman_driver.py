import argparse
import glob
import os
import re

from weatherman import WeatherReport


def validate_month(year_and_month):
    month = int(year_and_month.split('/')[1].replace('0', ''))
    if month < 13:
        return True


def validate_year_and_month(year_and_month):
    pattern = re.compile('\d{4}/\d{1,2}$')
    if pattern.match(year_and_month) and validate_month(year_and_month):
        return year_and_month
    else:
        raise argparse.ArgumentTypeError('{} is an invalid year/month value'.format(year_and_month))


def validate_year(year):
    pattern = re.compile('\d{4}$')
    if not pattern.match(year):
        raise argparse.ArgumentTypeError('{} is an invalid year'.format(year))
    else:
        return year


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', '--path', required=True)
    parser.add_argument('-e', help="Year", type=validate_year)
    parser.add_argument('-c', help="Year/month", type=validate_year_and_month)
    parser.add_argument('-a', help="Year/month", type=validate_year_and_month)
    parser.add_argument('-b', help="Year/month", type=validate_year_and_month)
    args = parser.parse_args()
    if args.a or args.b or args.c or args.e:
        args.path = args.path.split('-')[0]
        return args
    else:
        parser.exit(parser.print_help())


def main():
    args = parse_arguments()
    try:
        os.chdir(args.path)
        files_pattern = 'Murree_weather_*.txt'
        file_names = glob.glob(files_pattern)
        os.chdir("..")
    except FileNotFoundError:
        print('Files path is incorrect')
        return

    weather_report = WeatherReport(file_names)
    if args.e:
        weather_report.execute_first_task(args.e, args.path)
    if args.a:
        weather_report.execute_second_task(args.a, args.path)
    if args.c:
        weather_report.execute_third_task(args.c, args.path)
    if args.b:
        weather_report.execute_bonus_task(args.b, args.path)


if __name__ == "__main__":
    main()
