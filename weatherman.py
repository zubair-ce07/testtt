import argparse

from report_calculations import *


def main():
    arg_parser = argparse.ArgumentParser(description='Process some date')
    arg_parser.add_argument('path', type=str, nargs=1,
                            help='Collect the data from Directory')
    arg_parser.add_argument('-e',  type=validate_year, nargs=1,
                            help='Find the highest temperature and day, '
                                 'lowest temperature and day, most humid day '
                                 '(Single Month)')
    arg_parser.add_argument('-a', type=validate_year_month, nargs=1,
                            help='Find the average highest temperature,'
                                 ' average lowest temperature, average mean '
                                 'humidity (Range of Months)')
    arg_parser.add_argument('-c', type=validate_year_month, nargs=1,
                            help='Draws two horizontal bar charts for the'
                                 ' highest and lowest temperature on each  '
                                 'day. Highest in  red and lowest in blue. ('
                                 'Range of Months)')
    args = arg_parser.parse_args()
    if args.e:
        year_report = WeatherReport()
        year_report.file_read(args.path[0], args.e[0], '*')
        year_report.yearly_report()

    if args.a:
        year = datetime.strptime(args.a[0], "%Y/%m").strftime('%Y')
        month = datetime.strptime(args.a[0], "%Y/%m").strftime('%b')

        month_report = WeatherReport()
        month_report.file_read(args.path[0], year, month)
        month_report.monthly_report()

    if args.c:
        year = datetime.strptime(args.c[0], "%Y/%m").strftime('%Y')
        month = datetime.strptime(args.c[0], "%Y/%m").strftime('%b')

        daily_report = WeatherReport()
        daily_report.file_read(args.path[0], year, month)
        daily_report.daily_report()


def validate_year(date):
    if date:
        try:
            return datetime.strptime(date, "%Y").strftime("%Y")
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"{date} is an invalid year")


def validate_year_month(date):
    if date:
        try:
            return datetime.strptime(date, "%Y/%m").strftime("%Y/%m")
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"{date} is an invalid year/month input, '/' must be used as "
                f"separator between year and month")


if __name__ == "__main__":
    main()
