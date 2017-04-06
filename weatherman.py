"""This is a weatherman module
This module can calculate extremes (lowest, highest) of given calender year. 
It can also calculate average weather and display weather chart of a month 
"""
from __future__ import print_function

__author__ = "Jawad Tahir"

import getopt
import sys
import os
import csv
from os import path

dir_path = ''
files = []

USAGE_STRING = r'usage: weatherman <files directory> -opt1 arg1 [-opt2 arg2 [-opt3 arg3]]' + (
               '\nopt1, opt2, opt3: a, e, c' + '\narg1, arg2, arg3: Date\n'
)

MAX_TEMPRATURE = 'Max TemperatureC'
MIN_TEMPRATURE = 'Min TemperatureC'
MAX_HUMIDITY = 'Max Humidity'
MEAN_HUMIDITY = ' Mean Humidity'
DATE = 'PKT'
RED = '\033[91m'
BLUE = '\033[34m'
END = '\033[0m'
PLUS = '+'

month_name_dict = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}


def abort_unexpectedly(message):
    """Prints the error message and exit"""
    print(message)
    sys.exit(2)


def print_extreme_weather(date):
    """Prints extremes of the given year in YYYY format"""
    # Check if date is in proper format, throw error otherwise
    if len(date) != 4:
        abort_unexpectedly('Invalid date format. Use YYYY')

    highest_temp_row = ''
    highest_temp = -273.0
    lowest_temp_row = ''
    lowest_temp = 200.0
    most_humid_row = ''
    most_humid = 0.0
    file_found = False

    for file in files:
        # Create relative path of file
        relative_path = path.join(dir_path, file)
        # Check if child is file or directory
        if path.isfile(relative_path):
            # If file name contains the date
            if file.find(date) > 0:
                try:
                    file_obj = open(relative_path)
                except IOError as error:
                    abort_unexpectedly('Unable to open file', error.strerror)
                # Set the flag
                file_found = True
                reader = csv.DictReader(file_obj)
                for row in reader:
                    # Get the desired values from row
                    if row[MAX_TEMPRATURE] and float(row[MAX_TEMPRATURE]) > highest_temp:
                        highest_temp = float(row[MAX_TEMPRATURE])
                        highest_temp_row = row
                    if row[MAX_TEMPRATURE] and float(row[MIN_TEMPRATURE]) < lowest_temp:
                        lowest_temp = float(row[MIN_TEMPRATURE])
                        lowest_temp_row = row
                    if row[MAX_TEMPRATURE] and float(row[MAX_HUMIDITY]) > most_humid:
                        most_humid = float(row[MAX_HUMIDITY])
                        most_humid_row = row
                # Close file
                file_obj.close()
    # If some data is found, print it otherwise display error
    if file_found:
        print('Highest: %.1fC on %s %s' % (
            highest_temp, month_name_dict.get(int(highest_temp_row[DATE].split('-')[1])),
            highest_temp_row[DATE].split('-')[2]
        ))
        print('Lowest: %.1fC on %s %s' % (
            lowest_temp, month_name_dict.get(int(lowest_temp_row[DATE].split('-')[1])),
            lowest_temp_row[DATE].split('-')[2]
        ))
        print('Humidity: %.1f%% on %s %s' % (
            most_humid, month_name_dict.get(int(most_humid_row[DATE].split('-')[1])),
            most_humid_row[DATE].split('-')[2]
        ))
    else:
        print('No data found')

    print('\n')


def print_average_weather(date):
    """Prints average highest, lowest and mean humidity of date given in YYYY/MM format """
    # Check if date is in proper format (YYYY/MM)
    if len(date) < 6 and date.find(r'/') != 4:
        abort_unexpectedly('Invalid date format. Use YYYY/MM')
    # Extract month and year
    month = int(date.split(r'/')[1])
    year = int(date.split(r'/')[0])
    no_of_days = 0
    total_highest_temp = 0
    total_lowest_temp = 0
    total_mean_humid = 0
    file_found = False
    # Get english name of month
    month = month_name_dict.get(month)
    for file in files:
        # Create relative path of file
        relative_path = path.join(dir_path, file)
        # Check if child is file or directory
        if path.isfile(relative_path) and month:
            # If file name contains the date
            if file.find(str(year)) > 0 and file.find(str(month)) > 0:
                try:
                    file_obj = open(relative_path)
                except IOError as error:
                    abort_unexpectedly('Unable to open file', error.strerror)
                file_found = True
                reader = csv.DictReader(file_obj)
                for row in reader:
                    no_of_days += 1
                    if row[MAX_TEMPRATURE]:
                        total_highest_temp += float(row[MAX_TEMPRATURE])
                    if row[MIN_TEMPRATURE]:
                        total_lowest_temp += float(row[MIN_TEMPRATURE])
                    if row[MEAN_HUMIDITY]:
                        total_mean_humid += float(row[MEAN_HUMIDITY])
                # Close file object
                file_obj.close()
                # We don't need to traverse remaining files
                break
    # Check if data is found, print it otherwise display error
    if file_found:
        print('Highest average: %.2fC' % (float(total_highest_temp / no_of_days)))
        print('Lowest average: %.2fC' % float(total_lowest_temp / no_of_days))
        print('Average Mean Humidity: %.2f%%' % float(total_mean_humid / no_of_days))
    else:
        print('No data found')
    print('\n')


def print_weather_chart(date):
    """Prints weather charts for given date in YYYY/MM format"""
    # Check if date is in proper format (YYYY/MM)
    if len(date) < 6 and date.find(r'/') != 4:
        abort_unexpectedly('Invalid date format. Use YYYY/MM')
    # Extract month and year
    month = int(date.split(r'/')[1])
    year = int(date.split(r'/')[0])
    file_found = False
    # Get english name of month
    month = month_name_dict.get(month)
    for file in files:
        # Create relative path of file
        relative_path = path.join(dir_path, file)
        # Check if child is file or directory
        if path.isfile(relative_path) and month:
            # If file name contains the date
            if file.find(str(year)) > 0 and file.find(str(month)) > 0:
                # Try to open file
                try:
                    file_obj = open(relative_path)
                except IOError as error:
                    abort_unexpectedly('Unable to open file', error.strerror)
                file_found = True
                reader = csv.DictReader(file_obj)
                # Iterate rows
                for row in reader:
                    str_chart = ''
                    min_temp = 0
                    max_temp = 0
                    date_of_month = row[DATE].split('-')[2].strip().zfill(2)
                    # Get minimum and maximum temperature
                    if row[MIN_TEMPRATURE].strip() != '':
                        min_temp = int(row[MIN_TEMPRATURE])
                        if min_temp > 0:
                            str_chart = str_chart + BLUE + PLUS*min_temp + END
                    if row[MAX_TEMPRATURE].strip() != '':
                        max_temp = int(row[MAX_TEMPRATURE])
                        if max_temp > 0:
                            str_chart = str_chart + RED + PLUS*max_temp + END
                    print(date_of_month, str_chart + ' %iC - %iC' % (min_temp, max_temp))
                print('\n')
                # Close file
                file_obj.close()
                break
    if not file_found:
        print('No data found.\n')


def directory_sanity_check(directory_path):
    """Checks if the given directory_path is valid one for data files"""
    # Check if path is directory, throw error otherwise
    if not path.isdir(directory_path):
        abort_unexpectedly('invalid file directory: %s' % dir_path)
    # If there are no child then then we don't have right directory of file, throw error
    if len(os.listdir(directory_path)) == 0:
        abort_unexpectedly('No files in directory')


if __name__ == '__main__':
    # We will needing minimum 4 arguments to make it work
    if len(sys.argv) < 4:
        abort_unexpectedly(USAGE_STRING)
    # Get path where data files are placed
    dir_path = sys.argv[1]
    # Check if directory is OK
    directory_sanity_check(dir_path)
    # Get files from the directory
    files = os.listdir(dir_path)
    # Get command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[2:], 'ha:e:c:')
    except getopt.GetoptError as optionsError:
        print('Invalid options ', optionsError)
        abort_unexpectedly(USAGE_STRING)
    # Iterate over options
    for opt, arg in opts:
        # Print average weather
        if opt.strip() == '-a':
            print_average_weather(arg.strip())
        # Print extremes of the date
        elif opt.strip() == '-e':
            print_extreme_weather(arg.strip())
        # Print chart of the date
        elif opt.strip() == '-c':
            print_weather_chart(arg.strip())
        else:
            abort_unexpectedly(USAGE_STRING)