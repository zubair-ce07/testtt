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
        weather_files_record = self.collect_files(files_path)
        for file in weather_files_record:
            file_data = self.read_file_data(file)
            for day_weather_record in file_data:
                if len(day_weather_record) > 2:
                    if day_weather_record["Max TemperatureC"] and \
                            day_weather_record["Min TemperatureC"] and \
                            day_weather_record["Max Humidity"]:
                        weather_records.append(WeatherRecord(
                            day_weather_record))
        return weather_records
