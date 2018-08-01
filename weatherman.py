"""
Module is capable of reading data from a given data-set and is able
to generate two types of report with it
"""

import os
import argparse
from collections import defaultdict


MAX = 1
MIN = 2


def _max_min_wrapper(output_type, first, second):
    """
    Is able to return max or min value based on output_type from
    last two arguments, also checks if both are valid int

    Arguments:
        output_type (int): "max" for maximum value and "min for minimum value
        first (int): first value for the comparison
        second (str): second value for the comparison
    Returns:
        (int): max or min value from last two arguments, depends upon the output_type
    """
    if not second:
        return first

    if not first:
        return int(second)

    result = max if output_type == MAX else min
    return result(first, int(second))


class Weather(object):
    """
    Weather holds different properties of weather like
    max_temperature, min_temperature, max_humidity, min_humidity,
    and store date in a string format
    """

    def __init__(self):
        """
        Variables with prefix max hold negative value so any value
        would be greater and will get stored. Vice versa in min
        variables
        """

        self.max_temperature = None
        self.min_temperature = None
        self.max_humidity = None
        self.min_humidity = None
        self.date = None

    def recalculate_weather_values(self, max_temperature, min_temperature, max_humidity, min_humidity):
        """
        Takes new weather values, calculates appropriate results and
        stores it in member variables

        Arguments:
            max_temperature (str): max temperature in the data-set
            min_temperature (str): min temperature in the data-set
            max_humidity (str): max humidity in the data-set
            min_humidity (str): min humidity in the data-set
        """

        self.max_temperature = _max_min_wrapper(MAX, self.max_temperature, max_temperature)
        self.min_temperature = _max_min_wrapper(MIN, self.min_temperature, min_temperature)
        self.max_humidity = _max_min_wrapper(MAX, self.max_humidity, max_humidity)
        self.min_humidity = _max_min_wrapper(MIN, self.min_humidity, min_humidity)

    def recalculate_hottest_day(self, temp, date):
        """
        Finds the hottest day in the data-set

        Arguments:
            temp (str): the passed temperature
            date (str): date of the temperature
        """

        self.max_temperature = _max_min_wrapper(MAX, self.max_temperature, temp)
        if temp and self.max_temperature == int(temp):
            self.date = date


class ReportGenerator(object):
    """
    Responsible for processing weather data in a specific format,
    generating a report based on the processed data
    """

    def __init__(self, report_type, directory_path):
        """
        Arguments:
            report_type (int): Value can be either 1 for temperature
            and humidity report or 2 for hottest day report.
            directory_path (str): actual path to the data-set
        """

        self.report_type = report_type
        self.weather_data = defaultdict(Weather)
        self._standard_spacing = 16
        self.directory_path = directory_path

    def generate_report(self):
        """
        Generates report based on the member variable report_type

        Raises:
            OSError: If unable to open files
            UnicodeDecodeError: If unicode encoded file is provided
        """

        self._process_weather_data()
        if self.report_type == 1:
            self._print_temp_and_humidity_report()
        elif self.report_type == 2:
            self._print_hottest_day_report()

    def _print_temp_and_humidity_report(self):
        """
        Prints weather stats for every year in data-set
        """

        print_format = '{:<{}}{:<{}}{:<{}}{:<{}}{}'
        print(
            print_format.format(
                'Year', self._standard_spacing,
                'MAX Temp', self._standard_spacing,
                'MIN Temp', self._standard_spacing,
                'MAX Humidity', self._standard_spacing,
                'MIN Humidity'
            )
        )
        print('-'*76)

        for year, weather in sorted(self.weather_data.items(), key=lambda item: item[0]):
            print(
                print_format.format(
                    year, self._standard_spacing,
                    weather.max_temperature, self._standard_spacing,
                    weather.min_temperature, self._standard_spacing,
                    weather.max_humidity, self._standard_spacing,
                    weather.min_humidity
                )
            )

    def _print_hottest_day_report(self):
        """
        Prints hottest date for every year in data-set
        """

        print_format = '{:<{}}{:<{}}{}'
        print(
            print_format.format(
                'Year', self._standard_spacing, 'Date', self._standard_spacing, 'Temp'
            )
        )
        print('-'*36)

        for year, weather in sorted(self.weather_data.items(), key=lambda item: item[0]):
            print(
                print_format.format(
                    year, self._standard_spacing, weather.date, self._standard_spacing,
                    weather.max_temperature
                )
            )

    def _process_weather_data(self):
        """
        Based on the report_type, processes the data that is present
        in the directory_path and stores output in member variable
        weather_data

        Raises:
            OSError: If unable to open files
            UnicodeDecodeError: If unicode encoded file is provided
        """

        file_names = os.listdir(self.directory_path)

        for file_name in file_names:
            file_path = self.directory_path + file_name
            with open(file_path) as input_file:
                monthly_report = input_file.read()
                self._process_monthly_report(monthly_report)

    def _process_monthly_report(self, monthly_report):
        """
        Processes weather data of a given monthly report

        Arguments:
            monthly_report (str): the complete report file in string format
        """

        monthly_report = monthly_report.split('\n')

        # year can be found on first 4 characters of index 2
        year = monthly_report[2][:4]

        # 2 is for first record line and -2 is for last record line
        for daily_weather_data in monthly_report[2:-2]:
            daily_weather_data = daily_weather_data.split(',')
            if self.report_type == 1:
                self.weather_data[year].recalculate_weather_values(
                    daily_weather_data[1], daily_weather_data[3],
                    daily_weather_data[7], daily_weather_data[9]
                )
            else:
                self.weather_data[year].recalculate_hottest_day(
                    daily_weather_data[1], daily_weather_data[0]
                )


def check_dir(directory_path):
    """
    Validates if the argument directory actually exists

    Returns:
        (str): The directory if it exists

    Raises:
        argeparse.ArgumentError: If it is an invalid directory
    """

    if os.path.isdir(directory_path):
        return directory_path
    else:
        raise argparse.ArgumentError('{} is an invalid directory'.format(directory_path))


def main():

    parser = argparse.ArgumentParser()

    help_report = '[Report #]\n1 for Annual Max/Min Temperature\n2 for Hottest day of each year'
    parser.add_argument('report', help=help_report, type=int, choices=[1, 2])

    help_data_dir = '[data_dir]\nDirectory containing weather data files'
    parser.add_argument('data_dir', type=check_dir, help=help_data_dir)

    args = parser.parse_args()
    report_generator = ReportGenerator(args.report, args.data_dir)

    try:
        report_generator.generate_report()
    except OSError as error:
        print('OSError: {}'.format(error))
    except UnicodeDecodeError as error:
        print('UnicodeDecodeError: {}'.format(error))


if __name__ == '__main__':
    main()
