import csv
import glob
import os

from weather_record import WeatherRecord


class WeatherDataParser:
    required_fields = ["Max TemperatureC", "Min TemperatureC",
                       "Max Humidity", " Mean Humidity"]

    def parse(self, files_path):
        weather_records = []
        for files_path in glob.iglob(os.path.join(files_path, '*.txt')):
            with open(files_path) as weather_file:
                for weather_record in csv.DictReader(weather_file, delimiter=","):
                    if all(weather_record.get(field) for field in WeatherDataParser.required_fields):
                        weather_records.append(WeatherRecord(weather_record))

        return weather_records
