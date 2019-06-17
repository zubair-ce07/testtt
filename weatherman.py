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

# ArgumentParser object is being used to specify
# arguments types and reading from console
parser = argparse.ArgumentParser(description='Generate Weather Reports')

parser.add_argument('directory_path',
                    type=str, nargs='?', default='weatherfiles',
                    help='path to weather files directory' +
                         ' (default=weatherfiles)')
parser.add_argument('-a', type=str, help='-a argument')
parser.add_argument('-c', type=str, help='-c argument')
parser.add_argument('-e', type=str, help='-e argument')

args = parser.parse_args()

# If some option is specified, make a dict of all the
# specified time periods against that option [-a, -c, -e]
# as a key, fetch data against each time period and invoke
# the compute method from the Calculator instance to
# generate the required report
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

                # Create reader and calculator instances
                # Reader insatance reads the data at creation
                data_store = WeatherReader(args.directory_path, each_period)
                calculator_instance = Calculator()

                # Check if data is available against the given time frame
                if not len(data_store.data):
                    print("No values are available for the given time period!")
                    print('\n')
                    continue

                # Compute the results by passing request and data
                # as well as the required report type to the calculator
                result = calculator_instance.compute(data_store.data,
                                                     '-' + key,
                                                     each_period)

                # Calculator might return empty list as a result.
                if result:
                    print(result.print_results())

                print('\n')
