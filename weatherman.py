"""
This module generate annual weather reports from provided data

This module has a class 'ReportGenerator' and some utility functions
which read files from provided directory and create two types of reports
"""

import argparse
import os
from collections import defaultdict
from datetime import datetime
from enum import Enum


class Extrema(Enum):
    MIN = 1
    MAX = 2


class YearlyWeatherData:
    """
    This class is used for storing required weather
    statistics of a year
    """
    def __init__(self):
        self.year = None
        self.max_temperature = None
        self.min_temperature = None
        self.max_humidity = None
        self.min_humidity = None
        self.hottest_day = None


def _to_int(str_number):
    """
    This converts string to int

    Arguments:
        str_number (str): containing digits to convert

    Returns:
        result (int): int value of string or None in case exceptions occur
    """

    try:
        result = int(str_number)
    except (ValueError, TypeError):
        # if str can not be parsed to int return None
        result = None

    return result


def _get_extrema(first, second, extrema_type):
    """
    This is used to compare one int and one string containing digits
    and if conversion to int can't be done returns other int.
    return None if both are None.

    Arguments:
        first (int): number to compare
        second (str): string to compare
        extrema_type (Extrema): type of comparison

    Returns:
        result (int): result of comparison based on extrema_type or None if both are None
    """

    second = _to_int(second)
    result = None

    # if either one in None, other is returned.
    if first is None:
        result = second

    elif second is None:
        result = first

    # if both are not None and Max is to return
    elif extrema_type == Extrema.MAX:
        result = first if first >= second else second

    # if both are not None and Min is to return
    elif extrema_type == Extrema.MIN:
        result = second if first >= second else first

    return result


class ReportGenerator:
    """
    Reads weather data from provided directory and generate two types of reports
    1- Min, Max humidity and temperature annual report
    2- Max temperature and date of that day in a year
    """

    def __init__(self, directory):
        """
        Parse data from data files in directory
        Store required stats on yearly basis to create annual reports

        Arguments:
            directory (str): path to directory which contains data files
        """

        self.weather_data = defaultdict(lambda: YearlyWeatherData())

        # creating list of text files in given directory and generating their absolute paths
        data_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.txt')]

        # parsing every file in the list
        for file in data_files:
            self._parse_file(file)

    def _parse_file(self, file):
        """
        Reads data from the file. discards unwanted data. extracts daily data.

        Arguments:
            file (str): file from which data to read
        """

        # No need for FileNotFound as directory is already checked
        with open(file, 'r') as input_file:
            input_data = input_file.readlines()

            # Discarding first 2 and last line. Remaining contains data for one day.
            for line in input_data[2:-1]:
                daily_weather_data = line.split(',')
                self._process_daily_data(daily_weather_data)

    def _process_daily_data(self, daily_data):
        """
        It maintains yearly data by comparing with provided day's data.

        Arguments:
            daily_data (list): Weather for one day
        """

        # Parsing date string to datetime object
        date = datetime.strptime(daily_data[0], '%Y-%m-%d')

        # get yearly data from dictionary
        yearly_data = self.weather_data[date.year]

        # checks if this year was processed earlier or not
        if yearly_data.year is None:
            yearly_data.year = date.year

        # Compare previous and given day's stats
        max_temp = _get_extrema(yearly_data.max_temperature, daily_data[1], Extrema.MAX)
        min_temp = _get_extrema(yearly_data.min_temperature, daily_data[3], Extrema.MIN)
        max_humidity = _get_extrema(yearly_data.max_humidity, daily_data[7], Extrema.MAX)
        min_humidity = _get_extrema(yearly_data.min_humidity, daily_data[9], Extrema.MIN)

        # if given day's max temp is more than previous max then update hottest day and max temp
        if max_temp != yearly_data.max_temperature:
            yearly_data.hottest_day = date
            yearly_data.max_temperature = max_temp

        # if result of comparison is not the same then update
        if min_temp != yearly_data.min_temperature:
            yearly_data.min_temperature = min_temp

        if max_humidity != yearly_data.max_humidity:
            yearly_data.max_humidity = max_humidity

        if min_humidity != yearly_data.min_humidity:
            yearly_data.min_humidity = min_humidity

    def print_temp_report(self):
        """
        Prints Min Max for both Temperature and Humidity for
        each year in the data to generate report
        """

        print('{:12s}{:14s}{:14s}{:20s}{:20s}'.format('Year', 'Max Temp', 'Min Temp', 'Max Humidity', 'Min Humidity'))
        print('-'*72)

        for year, data in self.weather_data.items():

            print(
                '{}{:12}{:14}{:17}{:20}'.format(
                    year,
                    data.max_temperature,
                    data.min_temperature,
                    data.max_humidity,
                    data.min_humidity
                )
            )

    def print_hottest_days(self):
        """
        Prints Year along with max temperature and date of hottest day.
        """

        print('{:12s}{:16s}{:14s}'.format('Year', 'Date', 'Temp'))
        print('-'*32)

        for year, data in self.weather_data.items():
            print(
                '{:12s}{:16s}{:14}'.format(
                    str(year),
                    # converting datetime to string
                    data.hottest_day.strftime('%d/%m/%Y'),
                    str(data.max_temperature)
                )
            )


def check_directory(path):
    """
    checks if the directory at path exists or not.

    Arguments:
        path (str): absolute path of the directory

    Returns:
        path (str): path of the directory

    Raises:
        ArgumentTypeError: if directory does not exist
    """
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError('Directory Provided does not exists')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process weather data and generate reports.')
    parser.add_argument(
        'report_number',
        choices=[1, 2],
        type=int,
        help='1 for Annual Max/Min Temperature. 2 for Hottest day of each year'
    )
    parser.add_argument(
        'data_dir',
        type=check_directory,
        help='Directory containing weather data files'
    )
    args = parser.parse_args()

    # passing directory to ReportGenerator to parse the data.
    report_generator = ReportGenerator(args.data_dir)

    # Print report according to provided argument
    if args.report_number == 1:
        # print max min temp and humidity each year
        report_generator.print_temp_report()

    elif args.report_number == 2:
        # print max temp and date of hottest day
        report_generator.print_hottest_days()
