""" This is the driver program for the weatherman task.
    Having imported WeatherReader, reports and calculate
    classes from the WeatherReader.py file, it makes
    instances of those objects to achieve the tasks as
    specified by the command line arguments

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""

import sys
import argparse
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
else:
    options = {}
    if args.a:
        options.update({'a': x for x in [args.a] if x is not None})
    if args.c:
        options.update({'c': x for x in [args.c] if x is not None})
    if args.e:
        options.update({'e': x for x in [args.e] if x is not None})

    for key in options:
        for time_period_list in options.get(key).split():
            for one_time_period in time_period_list.split(','):

                my_weather_data = WeatherReader(args.dir_path, one_time_period)
                my_generator = ReportGenerator()

                if my_weather_data.data == ['year_error']:
                    print("Year value should be in full format e.g. 2014")
                    print('\n')
                    continue
                elif my_weather_data.data == ['month_error']:
                    print("Please enter a valid (1<month<13) value for month")
                    print('\n')
                    continue
                elif not len(my_weather_data.data):
                    print("No values are available for the given time period!")
                    print('\n')
                    continue

                report = my_generator.generate_report(my_weather_data.data,
                                                      '-' + key,
                                                      one_time_period)

                if report:
                    print(report.print_reports())

                print('\n')
