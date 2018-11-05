import csv
import glob
from datetime import datetime

from weather_records import WeatherRecords


class FileParser:
    """ Class for parsing the all weather files and returing the requried details """

    def read_all_weather_files(self, files_dir):
        all_weather_records = []

        for file in glob.glob(f"{files_dir}*.txt"):
            with open(file, "r") as file_data:
                file_reader = csv.DictReader(file_data)
                for instance in file_reader:
                    req_attrs = {
                        "Max Temperature": instance["Max TemperatureC"],
                        "Min Temperature": instance["Min TemperatureC"],
                        "Max Humidity": instance["Max Humidity"],
                        "Min Humidity": instance[" Min Humidity"],
                        "Mean Humidity": instance[" Mean Humidity"]}
                    date = instance.get("PKT", instance.get("PKST"))
                    req_attrs["Date"] = datetime.strptime(date, "%Y-%m-%d")
                    if all(req_attrs.values()):
                        all_weather_records.append(WeatherRecords(req_attrs))

        return all_weather_records
