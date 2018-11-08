import csv
import glob
from datetime import datetime

from weather_records import WeatherRecords


class FileParser:
    """ Class for parsing the all weather files and returing the requried details """

    def read_all_weather_files(self, files_dir):
        all_records = []

        for file_name in glob.glob(f"{files_dir}*.txt"):
            with open(file_name, "r") as file_data:
                for record in csv.DictReader(file_data):
                    attrs = self.requried_attrs(record)
                    if self.is_valid(attrs):
                        all_records.append(WeatherRecords(attrs))

        return all_records

    def requried_attrs(self, record):
        req_attrs = {
            "Max Temperature": record["Max TemperatureC"],
            "Min Temperature": record["Min TemperatureC"],
            "Max Humidity": record["Max Humidity"],
            "Min Humidity": record[" Min Humidity"],
            "Mean Humidity": record[" Mean Humidity"]}
        date = record.get("PKT") or record.get("PKST")
        req_attrs["Date"] = datetime.strptime(date, "%Y-%m-%d")

        return req_attrs

    def is_valid(self, attrs):
        return all(attrs.values())
