import os
import sys
import csv

class Parser:

    def parse_files(self, directory, files_to_parse):
        for file in files_to_parse:
            weather_file = open(directory + "/" + file)
            csv_reader = csv.DictReader(weather_file)
            weather_list = []
            for data in csv_reader:
                weather_list.append(data)

        return weather_list