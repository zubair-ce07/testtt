import weatherdata
import os
import csv


class DataParser:
    def __init__(self):
        self.data = []

    def get_data(self, file_path):
        try:
            all_files = [x for x in os.listdir(file_path) if x[-4:] == '.txt']

            for file_name in all_files:
                with open(file_path + "/" + file_name, "r") as weather_file:
                    csv_file = csv.DictReader(weather_file, delimiter=",")

                    for line in csv_file:
                        weather_data = weatherdata.WeatherData("NA", "NA",
                                                               "NA",
                                                               "NA", "NA",
                                                               "NA")
                        weather_data.set_all_members(line)
                        self.data.append(weather_data)

        except FileNotFoundError:
            print("Wrong path, no such directory exists!")
            return None

        return self.data
