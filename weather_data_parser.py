import csv
import fnmatch
import os
from pathlib import Path

from constants import CITY_NAME
from utilities import parse_date
from weather_reading import WeatherReading


class WeatherDataParser:

    def __init__(self, path):
        self.__path = path
        self.__records = []
        self.__load_data_from_files()

    def __load_data_from_files(self):
        files_to_read = self.__fetch_files_matching_pattern(f'{CITY_NAME}_weather_*.txt')

        for file in files_to_read:
            with open(Path(self.__path, file), 'r') as data_file:
                reader = csv.DictReader(data_file, skipinitialspace=True)

                for row in reader:
                    row = self.__preprocess_row(row)

                    self.__records.append(WeatherReading(reading_date=parse_date(row['PKT']),
                                                         max_temperature=row['Max TemperatureC'],
                                                         min_temperature=row['Min TemperatureC'],
                                                         mean_temperature=row['Mean TemperatureC'],
                                                         max_humidity=row['Max Humidity'],
                                                         min_humidity=row['Min Humidity'],
                                                         mean_humidity=row['Mean Humidity']))

    def fetch_records_of_month(self, month, year):
        records = []

        for record in self.__records:
            if record.reading_date.month == month and record.reading_date.year == year:
                records.append(record)

        return records

    def fetch_records_of_year(self, year):
        records = []

        for record in self.__records:
            if record.reading_date.year == year:
                records.append(record)

        return records

    def __preprocess_row(self, row):
        if 'PKT' not in row:
            row['PKT'] = row['PKST']
        return row

    def __fetch_files_matching_pattern(self, pattern):
        return fnmatch.filter(os.listdir(self.__path), pattern)
