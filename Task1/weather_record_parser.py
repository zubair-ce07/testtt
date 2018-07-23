import glob
import csv
import os

from weather_record import WeatherRecord


class WeatherDataParser:
    required_fields = ["Max TemperatureC", "Min TemperatureC", "Mean TemperatureC",
                       "Max Humidity", " Min Humidity"]

    def __init__(self):
        self.weather_records = []

    def parse(self, files_path):
        for file_name in glob.iglob(os.path.join(files_path, '*.txt')):
            with open(os.path.join(files_path, file_name), "r") as weather_file:
                for weather_record in csv.DictReader(weather_file, delimiter=","):
                    if all(weather_record.get(f) for f in WeatherDataParser.required_fields):
                        self.weather_records.append(WeatherRecord(weather_record))

        return self.weather_records
