import csv
import os

from weather_record import WeatherRecord


class WeatherDataParser:

    def collect_files(self, files_path):
        weather_files_record = []
        for file_name in os.listdir(files_path):
            if not file_name.startswith('.'):
                weather_files_record.append(files_path + file_name)
        return weather_files_record

    def read_file_data(self, file_path):
        file_data = []
        with open(file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                file_data.append(row)
        return file_data

    def parse(self, files_path):
        weather_records = []
        for file in self.collect_files(files_path):
            [weather_records.append(WeatherRecord(day_weather_record))
             for day_weather_record in self.read_file_data(file) if
             day_weather_record["Max TemperatureC"]]
        return weather_records
