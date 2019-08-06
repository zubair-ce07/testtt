import argparse
from datetime import datetime
from records import WeatherRecords
from reports import WeatherReports


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Provide path for files!')
    parser.add_argument('-e', nargs='*', help='Enter Year')
    parser.add_argument('-a', nargs='*', help='Enter year/month')
    parser.add_argument('-c', nargs='*', help='Enter year/month (charts)')

    args = parser.parse_args()
    record = WeatherRecords(args.path)

    if args.e:
        report = WeatherReports(record, int(args.e[0]))
        report.yearly_report()

    if args.a:
        arg = datetime.strptime(args.a[0], '%Y/%m')
        # print(arg.month, arg.year)
        report = WeatherReports(record, arg.year, arg.month)
        report.monthly_report()

    if args.c:
        arg = datetime.strptime(args.c[0], '%Y/%m')
        # print('in the c -->>>>> ', arg.month, arg.year)
        report = WeatherReports(record, arg.year, arg.month)
        report.monthly_report_chart()


if __name__ == '__main__':
    main()
