""" This is the driver program for the weatherman task.
    Having imported WeatherReader, reports and calculate
    classes from the WeatherReader.py file, it makes
    instances of those objects to achieve the tasks as
    specified by the command line arguments

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""

import sys
import argparse
from os.path import exists
from datareader import WeatherReader
from reportgenerator import ReportGenerator

parser = argparse.ArgumentParser(description='Generate Weather Reports')

parser.add_argument('dir_path',
                    type=str, nargs='?', default='weatherfiles',
                    help='path to weather files directory' +
                         ' (default=weatherfiles)')
parser.add_argument('-a', type=str, help='-a argument')
parser.add_argument('-c', type=str, help='-c argument')
parser.add_argument('-e', type=str, help='-e argument')

args = parser.parse_args()

if not args.a and not args.c and not args.e:
    print('Please specify one of [-a] [-e] [-c] to generate reports')
    exit()
elif not exists(args.dir_path):
    print("Directory does not exists!")
    exit()
else:
    options = {}
    if args.a:
        options.update({'a': x for x in [args.a] if x is not None})
    if args.c:
        options.update({'c': x for x in [args.c] if x is not None})
    if args.e:
        options.update({'e': x for x in [args.e] if x is not None})

    for report_type in options:
        for time_period_list in options.get(report_type).split():
            for one_time_period in time_period_list.split(','):
                year_month = one_time_period.split('/')
                year = year_month[0]
                month = ''
                if len(year_month) > 1:
                    if year_month[1]:
                        month = year_month[1]

                if int(year) < 1000 or int(year) > 9999:
                    print("Year value should be in full format e.g. 2014")
                    print('\n')
                    continue

                if report_type != 'e':
                    if not month or int(month) < 1 or int(month) > 13:
                        print("Enter a valid (1<month<13) value for month")
                        print('\n')
                        continue
                else:
                    if month:
                        print("You can't specify month value for -c")
                        print('\n')
                        continue

                my_weather_data = WeatherReader(args.dir_path, year, month)

                if not len(my_weather_data.data):
                    print("No values are available for the given time period!")
                    print('\n')
                    continue

                my_generator = ReportGenerator()
                report = my_generator.generate_report(my_weather_data.data,
                                                      '-' + report_type,
                                                      one_time_period)

                if report:
                    print(report.print_reports())

                print('\n')
