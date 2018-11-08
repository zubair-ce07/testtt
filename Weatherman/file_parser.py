import csv
import glob

from weather_records import WeatherRecords


class FileParser:
    """ Class for parsing the all weather files and returing the requried details """

    def read_all_weather_files(self, files_dir):
        all_records = []

        for file_name in glob.glob(f"{files_dir}*.txt"):
            with open(file_name, "r") as file_data:
                reader = csv.DictReader(file_data)
                [all_records.append(WeatherRecords(record)) for record in reader if self.is_valid_record(record)]

        return all_records

    def is_valid_record(self, record):
        req_attrs = [
            record["Max TemperatureC"], record["Min TemperatureC"],
            record["Max Humidity"], record[" Min Humidity"],
            record[" Mean Humidity"]]

        return all(req_attrs)
