import os
from abc import ABC, abstractmethod

from weatherdata import WeatherData


class WeatherParser(ABC):

    @abstractmethod
    def parse(self):

        raise NotImplementedError()


class YearlyWeatherParser(WeatherParser):

    def __init__(self, path, year):

        self.path = path
        self.year = year
        self.weather_data = []

    def parse(self):

        file_names = os.listdir(path=self.path)

        for file_name in file_names:

            current_file_year = int(file_name.split('_')[2])

            if current_file_year == self.year:
                current_file_path = os.path.join(self.path, file_name)

                with open(current_file_path, mode='r') as file_data:
                    file_contents = file_data.read()
                    records = file_contents.split('\n')
                    records = records[1:-1]

                    for record in records:
                        record = record.split(',')

                        self.weather_data.append(WeatherData(
                            pkt=record[0],
                            max_temp=int(record[1]) if record[1] is not '' else None,
                            min_temp=int(record[3]) if record[3] is not '' else None,
                            max_humidity=int(record[7]) if record[7] is not '' else None
                        ))

        return self.weather_data


class MonthlyWeatherParser(WeatherParser):

    _months_abbr = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                    'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    def __init__(self, path, year, month):

        self.path = path
        self.month = month
        self.year = year
        self.weather_data = []

    def parse(self):

        file_names = os.listdir(path=self.path)

        for file_name in file_names:

            current_file_month = self._months_abbr.index(file_name.split('_')[3][:3].lower()) + 1
            current_file_year = int(file_name.split('_')[2])

            if current_file_month == self.month and current_file_year == self.year:
                current_file_path = os.path.join(self.path, file_name)

                with open(current_file_path, mode='r') as file_data:
                    file_contents = file_data.read()
                    records = file_contents.split('\n')
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
