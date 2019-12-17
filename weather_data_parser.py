import csv
import glob
from datetime import datetime

from constants import CITY_NAME, COLUMN_NAMES, COLUMNS_TO_VALIDATE
from weather_reading import WeatherReading


class WeatherDataParser:

    def __init__(self, path):
        self.__path = path
        self.__records = []
        self.__load_data_from_files()

    def __load_data_from_files(self):
        files_to_read = self.__fetch_files_matching_pattern(f'{self.__path}/{CITY_NAME}_weather_*.txt')

        for file in files_to_read:
            with open(file, 'r') as data_file:
                reader = csv.DictReader(data_file, fieldnames=COLUMN_NAMES)
                next(reader)

                for row in reader:
                    row = self.__preprocess_row(row)

                    if row is not None:
                        self.__records.append(WeatherReading(row))

    def fetch_records(self):
        return self.__records

    def __preprocess_row(self, row):
        try:
            for column in COLUMNS_TO_VALIDATE:
                if column == 'PKT':
                    row[column] = datetime.strptime(row[column], '%Y-%m-%d')
                elif row[column] != '':
                    row[column] = float(row[column])
                else:
                    return None

            return row
        except ValueError:
            return None

    def __fetch_files_matching_pattern(self, pattern):
        return glob.glob(pattern)
