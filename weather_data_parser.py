import csv
import glob

from constants import CITY_NAME, COLUMN_NAMES
from utilities import parse_date, str_to_float
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

                    self.__records.append(WeatherReading(row))

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
        for column in COLUMN_NAMES:
            if column == 'PKT':
                row[column] = parse_date(row[column], '%Y-%m-%d')
            else:
                row[column] = str_to_float(row[column])
        return row

    def __fetch_files_matching_pattern(self, pattern):
        return glob.glob(pattern)
