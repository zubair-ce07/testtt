import csv
import glob
import os

from weather_record import WeatherRecord


class WeatherDataParser:
    required_fields = ["Max TemperatureC", "Min TemperatureC",
                       "Max Humidity", " Mean Humidity"]

    def read_file_data(self, file_path):
        file_data = []
        with open(file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                file_data.append(row)
        return file_data

    def parse(self, files_path):
        weather_records = []
        for file_name in glob.iglob(os.path.join(files_path, '*.txt')):
            for day_weather_record in self.read_file_data(file_name):
                if all(day_weather_record.get(field) for field in WeatherDataParser.required_fields):
                    weather_records.append(WeatherRecord(day_weather_record))
        return weather_records
