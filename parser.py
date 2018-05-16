import os
import sys
import csv
import fnmatch

class Parser:

    @staticmethod
    def parse_files(directory, file_name_pattern):
        files_to_parse = []
        weather_list = []
        for file in os.listdir(directory):
            if fnmatch.fnmatch(file, '*'+file_name_pattern+'*'):
                files_to_parse.append(file)

        for file in files_to_parse:
            with open(f"{directory}/{file}") as weather_file:
                csv_reader = csv.DictReader(weather_file)
                for data in csv_reader:
                    weather_list.append(data)
        
        for reading in weather_list:
            reading = {k.strip(): v for k, v in reading.items()}

        return weather_list
