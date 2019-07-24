import csv
import glob
from record import WeatherData


class FileParser:

    years = []

    @staticmethod
    def record_values(self, record):
        valid_record = [record["Max TemperatureC"], record["Min TemperatureC"],
                        record[" Mean Humidity"], record.get("PKT", record.get("PKST"))]
        if all(valid_record):
            return True

    def file_reader(self, files_path):
        records = []
        files_path += f"Murree_weather_*"
        for files in glob.glob(files_path):

            with open(files, "r") as single_file:
                file_reader = csv.DictReader(single_file)
                records += [WeatherData(row) for row in file_reader if self.record_values(self, row)]
        return records
