import csv
import glob


from constants import CITY_NAME, CSV_HEADERS_MAPPING
from weather_record import WeatherRecord


class WeatherDataParser:

    def __init__(self, path):
        self.__path = path
        self.__weather_records = []

    def load_data_from_files(self):
        files_to_read = self.__fetch_files_matching_pattern(f'{self.__path}/{CITY_NAME}_weather_*.txt')

        for file in files_to_read:
            with open(file, 'r') as data_file:
                reader = csv.DictReader(data_file)
                csv_headers = reader.fieldnames

                for index, header in enumerate(reader.fieldnames):
                    matching_header = next((header_key for header_key, mapped_header_list in CSV_HEADERS_MAPPING.items()
                                           if header.strip() in mapped_header_list), header)

                    csv_headers[index] = matching_header

                reader.fieldnames = csv_headers
                for row in reader:
                    if self.__row_is_valid(row):
                        self.__weather_records.append(WeatherRecord(row))

    def fetch_records(self):
        return self.__weather_records

    def __row_is_valid(self, row):
        return all(value != '' for key, value in row.items() if key in CSV_HEADERS_MAPPING.keys())

    def __fetch_files_matching_pattern(self, pattern):
        return glob.glob(pattern)
