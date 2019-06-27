"""
Module has all types of required parsers for the weatherman dataset
"""

import os
from abc import ABC, abstractmethod

from weatherdata import WeatherData


class WeatherParser(ABC):
    """
    Contract for all the classes that want to parse the weatherman
    dataset
    """

    @abstractmethod
    def parse(self):
        """
        Abstract method for the inheriting class to implement that will
        be responsible for parsing and returning the data

        Returns:
            (list): List of WeatherMan type
        """

        pass


class YearlyWeatherParser(WeatherParser):
    """
    Parses the data on a yearly basis
    """

    def __init__(self, path, year):
        """
        Constructor function

        Arguments:
            path (str): path to the weatherman dataset
            year (int): year for which the data needs to be filtered
        """

        self.path = path
        self.year = year
        self.weather_data = []

    def parse(self):

        # all the file names in the weatherman directory
        file_names = os.listdir(path=self.path)

        for file_name in file_names:

            # file_name is of the format Murree_weather_2004_Jun.txt
            current_file_year = int(file_name.split('_')[2])

            if current_file_year == self.year:
                current_file_path = os.path.join(self.path, file_name)

                with open(current_file_path, mode='r') as file_data:
                    file_contents = file_data.read()
                    records = file_contents.split('\n')

                    # first row contains title of each column and last
                    # row contains and empty line
                    records = records[1:-1]

                    for record in records:
                        record = record.split(',')

                        # the indexes are calculated after observing
                        # the dataset
                        self.weather_data.append(WeatherData(
                            pkt=record[0],
                            max_temp=int(record[1]) if record[1] is not '' else None,
                            min_temp=int(record[3]) if record[3] is not '' else None,
                            max_humidity=int(record[7]) if record[7] is not '' else None
                        ))

        return self.weather_data


class MonthlyWeatherParser(WeatherParser):
    """
    Parses the data on a monthly basis
    """

    _months_abbr = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                    'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    def __init__(self, path, year, month):
        """
        Constructor function

        Arguments:
            path (str): path to the weatherman dataset
            year (int): year for which the data needs to be filtered
            month (int): month for which the data needs to be filtered
        """

        self.path = path
        self.month = month
        self.year = year
        self.weather_data = []

    def parse(self):

        # all the file names in the weatherman directory
        file_names = os.listdir(path=self.path)

        for file_name in file_names:

            # file_name is of the format Murree_weather_2004_Jun.txt
            #
            # we need to get the month from file_name then lowercase
            # it then get its index. The index would be 1 less than
            # actual month count so need to add 1
            current_file_month = self._months_abbr.index(file_name.split('_')[3][:3].lower()) + 1
            current_file_year = int(file_name.split('_')[2])

            if current_file_month == self.month and current_file_year == self.year:
                current_file_path = os.path.join(self.path, file_name)

                with open(current_file_path, mode='r') as file_data:
                    file_contents = file_data.read()
                    records = file_contents.split('\n')

                    # first row contains title of each column and last
                    # row contains and empty line
                    records = records[1:-1]

                    for record in records:
                        record = record.split(',')
                        self.weather_data.append(WeatherData(
                            pkt=record[0],
                            max_temp=int(record[1]) if record[1] is not '' else None,
                            min_temp=int(record[3]) if record[3] is not '' else None,
                            mean_humidity=int(record[8]) if record[8] is not '' else None
                        ))

        return self.weather_data
