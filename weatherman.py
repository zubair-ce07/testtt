import argparse

from report_calculations import *


def main():
    arg_parser = argparse.ArgumentParser(description='Process some date')
    arg_parser.add_argument('path', type=str,
                            help='Collect the data from Directory')
    arg_parser.add_argument('-e',  type=lambda a: datetime.strptime(a, '%Y'),
                            help='Find the highest temperature and day, '
                                 'lowest temperature and day, most humid day '
                                 '(Single Month)')
    arg_parser.add_argument('-a', type=lambda a: datetime.strptime(a, '%Y/%m'),
                            help='Find the average highest temperature,'
                                 ' average lowest temperature, average mean '
                                 'humidity (Range of Months)')
    arg_parser.add_argument('-c', type=lambda a: datetime.strptime(a, '%Y/%m'),
                            help='Draws two horizontal bar charts for the'
                                 ' highest and lowest temperature on each  '
                                 'day. Highest in  red and lowest in blue. ('
                                 'Range of Months)')

    args = arg_parser.parse_args()
    if args.e:
        year_report = WeatherReport()
        year_report.file_read(args.path)
        year_report.yearly_report(args.e.year)

    if args.a:
        month_report = WeatherReport()
        month_report.file_read(args.path)
        month_report.monthly_report(args.a.year, args.a.strftime('%b'))

    if args.c:
        daily_report = WeatherReport()
        daily_report.file_read(args.path)
        daily_report.daily_report(args.c.year, args.c.strftime('%b'))


if __name__ == "__main__":
    main()
