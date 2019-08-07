import csv
import os

from task2.reading import Reading
from task2.weather import Weather


class FileUtility:
    """ Utility to read all files in a directory and parse the contents """
    @staticmethod
    def parse_files(dir_name):
        weathers = []
        if os.path.isdir(dir_name):
            content = os.listdir(dir_name)
            for file_name in content:
                if os.path.isfile(dir_name + file_name):
                    new_weather = Weather()
                    with open(dir_name + file_name) as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        for index, row in enumerate(csv_reader):
                            if index > 0:
                                new_reading = Reading(*row)
                                new_weather.add_reading(new_reading)
                    weathers.append(new_weather)
        else:
            print(f"{dir_name} not a directory")
        return weathers
