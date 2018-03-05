"""
This module contains different functions for calculating different reports and
showing charts for temperature records from 1996-2011
"""
import argparse
import calendar
import glob
from datetime import datetime

import constants


def yearly_report(year=None):
    """
    This function gets all the files for months of a year and find max,
    min temp and max humidity across a year and displays with date
    :param year: Year for which we want to print calculations
    :return: None
    """
    if not year or year < 1996 or year > 2011:
        print(constants.NO_DATA_ABAILABLE_MSG)
        exit()

    # Getting all files name which contain data for given year
    files_for_year = 'weatherdata/lahore_weather_{}_*.txt'.format(year)
    files = glob.glob(files_for_year)

    # Reading data from files
    data = read_and_return_data(files)

    print('Printing Statistics For Year {}'.format(year))
    max_temp = max([sublist[1] for sublist in data if sublist[1]
                    not in constants.NULLS])
    date_max_temp = [sublist[0] for sublist in data if
                     sublist[1] == max_temp][-1]
    date_max_temp = convert_date_to_alphabetical_month(date_max_temp)

    min_temp = min([sublist[2] for sublist in data if sublist[2]
                    not in constants.NULLS])
    date_min_temp = [sublist[0] for sublist in data if
                     sublist[2] == min_temp][-1]
    date_min_temp = convert_date_to_alphabetical_month(date_min_temp)

    max_hum = max([sublist[3] for sublist in data if sublist[3]
                   not in constants.NULLS])
    date_max_hum = [sublist[0] for sublist in data if
                    sublist[3] == max_hum][-1]
    date_max_hum = convert_date_to_alphabetical_month(date_max_hum)

    # Printing desired calculations on console
    print('Highest: {temp}C on {date}'.format(
        temp=max_temp, date=date_max_temp))
    print('Lowest: {temp}C on {date}'.format(
        temp=min_temp, date=date_min_temp))
    print('Humid: {hum}% on {date}'.format(
        hum=max_hum, date=date_max_hum))


def convert_date_to_alphabetical_month(date):
    """
    This function simply takes a string date and convert it to string
    with month name
    :param date:
    :return: date with month name in alphabets
    """
    _date = datetime.strptime(date, '%Y-%m-%d')
    _date = datetime.strftime(_date, '%B %d')

    return _date


def read_and_return_data(files=None):
    """
    This method gets a list of file names and iterates over all the files and
    reads rows but stores data required for calculations in a separate lists.
    :param files: List of files names to read data from
    :return: A List of Tuples (Each tuple contains a date, max, min temperature
    on that date and max humidity on that date)
    """
    data = list()
    for file in files:
        with open(file) as file_read:
            # Skipping first line as it is empty for all files
            file_read.readline()
            # Saving header of file
            header = file_read.readline().split(',')
            header = [field.strip() for field in header]

            # Read all lines of file
            for line in file_read:
                values = line.split(',')
                if len(values) != len(header):
                    pass
                else:
                    # Get index of fields from header and get value at that
                    # index in values list and make a new record and append
                    # into data list.
                    try:
                        date = values[header.index(constants.DATE_LABEL)]
                    except ValueError:
                        date = values[header.index(constants.DATE_LABEL_2)]
                    max_temp = values[header.index(constants.MAX_TEMP_LABEL)]
                    min_temp = values[header.index(constants.MIN_TEMP_LABEL)]
                    max_humid = values[header.index(
                        constants.MAX_HUMIDITY_LABEL)]

                    data.append((date, max_temp, min_temp, max_humid))

    return data


def monthly_average_report(year_and_month=None):
    """
    This function gets all the files with data against a year and month
    and calculates average max_temp, min_temp and max_humidity and prints
    the calculations.
    :param year_and_month: Year and month against which we want to calculate
    :return: None
    """
    year_and_month = year_and_month.split('/')
    year = int(year_and_month[0])
    month = int(year_and_month[1])
    month = calendar.month_abbr[month]
    if not year or year < 1996 or year > 2011:
        print(constants.NO_DATA_ABAILABLE_MSG)
        exit()

        # Getting all files name which contain data for given year
    files_for_year = 'weatherdata/lahore_weather_{}_{}.txt'.format(year, month)
    files = glob.glob(files_for_year)

    data = read_and_return_data(files)

    average_max_temp = sum([int(sublist[1]) for sublist in data])/len(data)
    average_min_temp = sum([int(sublist[2]) for sublist in data])/len(data)
    average_max_hum = sum([int(sublist[3]) for sublist in data])/len(data)

    print('Printing Statistics For {}, {}'.format(month, year))
    print('Highest Average: {}C'.format(int(average_max_temp)))
    print('Lowest Average: {}C'.format(int(average_min_temp)))
    print('Average Humidity: {}%'.format(int(average_max_hum)))


def monthly_charts_report(year_and_month=None, same=False):
    """
    This function gets all the files with data against a year and month
    and calculates average max_temp, min_temp and max_humidity and prints
    the charts like output on terminal.
    :param year_and_month: Year and month against which we want to calculate
    :param same: Parameter to decide if we want to print both min and max at
    same line or not.
    :return: None
    """
    year_and_month = year_and_month.split('/')
    year = int(year_and_month[0])
    month = int(year_and_month[1])
    month = calendar.month_abbr[month]
    if not year or year < 1996 or year > 2011:
        print(constants.NO_DATA_ABAILABLE_MSG)
        exit()

        # Getting all files name which contain data for given year
    files_for_year = 'weatherdata/lahore_weather_{}_{}.txt'.format(year, month)
    files = glob.glob(files_for_year)

    data = read_and_return_data(files)

    print('Printing Statistics For {}, {}'.format(month, year))

    if not same:
        for day in data:
            print('{day} {color} {asterisk} {end} {temp}C'.format(
                day=day[0].split('-')[-1],  color=constants.RED_COLOR_ANSI,
                asterisk=create_chars(day[1]), temp=day[1],
                end=constants.END_COLOR))

            print('{day} {color} {asterisk} {end} {temp}C'.format(
                day=day[0].split('-')[-1], color=constants.BLUE_COLOR_ANSI,
                asterisk=create_chars(day[2]), temp=day[2],
                end=constants.END_COLOR))
    else:
        # BONUS TASK : It prints both min-max temp at same
        # line with different color charts
        for day in data:
            print('{day} {color_blue}{asterisk_min}{end}{color_red}'
                  '{asterisk_max}{end} {temp_min}C-{temp}C'.format(
                    day=day[0].split('-')[-1],
                    color_red=constants.RED_COLOR_ANSI,
                    color_blue=constants.BLUE_COLOR_ANSI,
                    asterisk_min=create_chars(day[2]),
                    asterisk_max=create_chars(day[1]),
                    temp=day[1], temp_min=day[2], end=constants.END_COLOR))


def create_chars(num=1):
    """
    Take a num and makes a string with that many repeating characters
    :param num: number of repeating characters we want
    :return: String with repeating characters of length num
    """
    if num in constants.NULLS:
        return ''
    if type(num) is not int:
        num = int(num)
    return '+' * num


def main():
    """
    This is our main method that will parse our arguments given and drive
    our script forward.
    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--yearly', type=int)
    parser.add_argument('-a', '--monthly_average', type=str)
    parser.add_argument('-c', '--monthly_charts', type=str)
    parser.add_argument('-cs', '--monthly_charts_same', type=str)
    args = parser.parse_args()

    if not (args.yearly or args.monthly_average or
            args.monthly_charts or args.monthly_charts_same):
        print(constants.NO_ARG_ERROR_MSG)
    elif args.yearly:
        yearly_report(year=args.yearly)
    elif args.monthly_average:
        monthly_average_report(year_and_month=args.monthly_average)
    elif args.monthly_charts:
        monthly_charts_report(year_and_month=args.monthly_charts)
    elif args.monthly_charts_same:
        # Bonus : It will print both temperatures charts on same line
        monthly_charts_report(year_and_month=args.monthly_charts_same,
                              same=True)

if __name__ == '__main__':
    main()
