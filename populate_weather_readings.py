import os
import csv
from itertools import islice
from weather_reading_data_structure import WeatherReading

_months_dictionary = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May",
                      6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct",
                      11: "Nov", 12: "Dec"}


class WeatherReadingsPopulator:

    def __init__(self, files_path):
        self.files_path = files_path
        self.weather_readings = []
        self.files = []

    def list_files(self,
                   report_type: str,
                   year: str,
                   month: object = str):
        self.files.clear()
        names_of_all_files = os.listdir(self.files_path)
        for file in names_of_all_files:
            if report_type == "-e":
                if file.find(str(year)) is not -1:
                    self.files.append(file)
            elif report_type in ["-a", "-c"]:
                if (file.find(year) is not -1
                        and file.find(_months_dictionary[month]) is not -1):
                    self.files.append(file)
                    break  # only one file needed

    def populate_weather_readings(self):
        self.weather_readings.clear()
        for file in self.files:
            with open(self.files_path+"/"+file) as f:
                reader = csv.reader(f)
                for row in islice(reader, 1, None):
                    weather_reading = WeatherReading(
                        row[0],
                        int(row[1])
                        if row[1] else None,
                        int(row[2])
                        if row[2] else None,
                        int(row[3])
                        if row[3] else None,
                        int(row[7])
                        if row[7] else None,
                        int(row[8])
                        if row[8] else None,
                        int(row[9])
                        if row[9] else None
                    )
                    self.weather_readings.append(weather_reading)
