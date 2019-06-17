""" This is the driver program for the weatherman task.
    Having imported WeatherReader, results and calculate
    classes from the WeatherReader.py file, it makes
    instances of those objects to achieve the tasks as
    specified by the command line arguments

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""

import sys
from weatherReader import WeatherReader
from weatherReader import Calculator

dir_path = sys.argv[1]
option = sys.argv[2]
request = sys.argv[3]

# If more than one report is to be generated
if len(sys.argv) > 4:
    for index in range(2, len(sys.argv), 2):
        # Get command line arguments
        option = sys.argv[index]
        request = sys.argv[index+1]

        # Create reader and calculator instances
        # Reader insatance reads the data at creation
        data_store = WeatherReader(dir_path, request)
        calculator_instance = Calculator()

        # Check if data is available against the given time frame
        if not len(data_store.data):
            print("No values are available for the given time period!")
            print('\n')
            continue

        # Compute the results by passing request and data
        # as well as the required report type to the calculator
        result = calculator_instance.compute(data_store.data, option, request)

        # Calculator might return empty list as a result.
        if result:
            print(result.print_results())

        print('\n')

# If there is only one report to be generated
else:
    # Create reader and calculator instances
    # Reader insatance reads the data at creation
    data_store = WeatherReader(dir_path, request)
    calculator_instance = Calculator()

    # Check if data is available against the given time frame
    if not len(data_store.data):
        print("No values are available for the given time period!")
        exit()

    # Compute the results by passing request and data
    # as well as the required report type to the calculator
    result = calculator_instance.compute(data_store.data, option, request)

    # Calculator might return empty list as a result.
    if result:
        print(result.print_results())
