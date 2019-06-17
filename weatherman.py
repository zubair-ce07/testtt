""" This is the driver program for the weatherman task.
    Having imported WeatherReader, results and calculate
    classes from the WeatherReader.py file, it makes
    instances of those objects to achieve the tasks as
    specified by the command line arguments

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""

import sys
import argparse
from weatherReader import WeatherReader
from weatherReader import Calculator

parser = argparse.ArgumentParser(description='Generate Weather Reports')

parser.add_argument('directory_path',
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
        for period_list in options.get(key).split():
            for each_period in period_list.split(','):

                data_store = WeatherReader(args.directory_path, each_period)
                calculator_instance = Calculator()

                if data_store.data == ['year_error']:
                    print("Year value should be in full format e.g. 2014")
                    print('\n')
                    continue
                elif data_store.data == ['month_error']:
                    print("Please enter a valid (1<month<13) value for month")
                    print('\n')
                    continue
                elif not len(data_store.data):
                    print("No values are available for the given time period!")
                    print('\n')
                    continue

                result = calculator_instance.compute(data_store.data,
                                                     '-' + key,
                                                     each_period)

                if result:
                    print(result.print_results())

                print('\n')
