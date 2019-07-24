import csv
import glob

from weather_record import WeatherData


class FileParser:
    required_fields = ["Max TemperatureC", "Min TemperatureC", "Mean TemperatureC",
                       "Max Humidity", " Min Humidity"]

    def __init__(self):
        self.weather_records = []

    def file_reader(self, files_path):
        files_path += f"Murree_weather_*"
        for files in glob.glob(files_path):
            with open(files, "r") as weather_file:
                for weather_record in csv.DictReader(weather_file):
                    if all(weather_record.get(row) for row in FileParser.required_fields):
                        self.weather_records.append(WeatherData(weather_record))
        return self.weather_records
