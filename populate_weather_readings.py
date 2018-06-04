import os
from itertools import islice

_months_dictionary={1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May",
                    6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct",
                    11: "Nov", 12: "Dec"}


class WeatherReadingsPopulator:

    def __init__(self):
        self.weather_readings = []
        self.files = []

    def list_files(self, path: "files directory",
                   report_type: "required to populate relevant days' data",
                   year, month=None):
        names_of_all_files = os.listdir(path)
        for file in names_of_all_files:
            if report_type == "-e":
                if file.find(str(year)) is not -1:
                    self.files.append(file)
            elif report_type in ["-a", "-c"]:
                if (file.find(year) is not -1
                        and file.find(_months_dictionary[month]) is not -1):
                    self.files.append(file)
                    break

    def populate_weather_readings(self, path: "files directory"):
        for file in self.files:
            f = open(path+"/"+file)
            for line in islice(f, 1, None):
                weather_reading_from_line = line.split(",")
                weather_reading = [
                    weather_reading_from_line[0],[
                        int(weather_reading_from_line[1])
                        if weather_reading_from_line[1] else None,
                        int(weather_reading_from_line[2])
                        if weather_reading_from_line[2] else None,
                        int(weather_reading_from_line[3])
                        if weather_reading_from_line[3] else None
                    ],[
                        int(weather_reading_from_line[7])
                        if weather_reading_from_line[7] else None,
                        int(weather_reading_from_line[8])
                        if weather_reading_from_line[8] else None,
                        int(weather_reading_from_line[9])
                        if weather_reading_from_line[9] else None
                    ]
                ]
                self.weather_readings.append(weather_reading)




