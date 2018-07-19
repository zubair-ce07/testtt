import glob
import csv
import os

from weather_record import WeatherRecord


class WeatherDataParser:

    required_fields = ["Max TemperatureC", "Min TemperatureC", "Mean TemperatureC",
                       "Max Humidity", " Min Humidity"]

    def __init__(self):
        self.weather_records = []

    def parse(self, files_path, year, month=None):
        for file_name in glob.iglob(os.path.join(files_path, '*.txt')):
            with open(os.path.join(files_path, file_name), "r") as weather_file:
                weather_readings = csv.DictReader(weather_file, delimiter=",")

                for weather_record in weather_readings:
                    if all(weather_record.get(f) for f in WeatherDataParser.required_fields):
                        weather_record = WeatherRecord(weather_record)

                        if (weather_record.date.month == month if month else True) \
                                and weather_record.date.year == year:
                            self.weather_records.append(weather_record)

        if not self.weather_records:
            raise EOFError("No Record Exists for the given date")

        return self.weather_records
