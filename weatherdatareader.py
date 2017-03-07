import calendar
import csv
import glob
from dataoperations import DataOperations


class WeatherDataReader:

    def __init__(self):
        pass

    @staticmethod
    def read_single_file(file_path):
        with open(file_path, 'r') as weather_record_file:
            next(weather_record_file)  # Skipping Empty Line
            # Read File as List of Dictionaries
            weather_record_reader = csv.DictReader(weather_record_file)

            weather_records = list(weather_record_reader)
            weather_records.pop()  # Skip Footer

            return DataOperations.data_type_conversion(weather_records)

    @staticmethod
    def find_files(path, year, month):
        files = glob.glob('{path}/*{year}*{month}*.txt'.format(
            path=path, year=year, month=month))

        return files

    @staticmethod
    def read_file(path, year, month):
        month = calendar.month_name[month][:3]

        files = WeatherDataReader.find_files(path, year, month)

        weather_records = []
        # Find all files that matches the given pattern
        for file_name in files:
            weather_records.extend(WeatherDataReader.read_single_file(file_name))

        return weather_records
