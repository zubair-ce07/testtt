import csv
import glob
from datetime import datetime

from weather_records import WeatherRecords


class FileParser:
    """ Class for parsing the all weather files and returing the requried details """

    def read_all_weather_files(self, files_dir):
        all_records = []

        for file_tag in glob.glob(f"{files_dir}*.txt"):
            with open(file_tag, "r") as file_data:
                reader = csv.DictReader(file_data)
                [all_records.append(WeatherRecords(
                    self.get_record(record))) for record in reader if self.get_record(record)]

        return all_records

    def get_record(self, record):
        req_attrs = {
            "Max Temperature": record["Max TemperatureC"],
            "Min Temperature": record["Min TemperatureC"],
            "Max Humidity": record["Max Humidity"],
            "Min Humidity": record[" Min Humidity"],
            "Mean Humidity": record[" Mean Humidity"]}
        date = record.get("PKT") or record.get("PKST")
        req_attrs["Date"] = datetime.strptime(date, "%Y-%m-%d")

        if not all(req_attrs.values()):
            return False

        return req_attrs
