import csv
import os

from task2.reading import Reading
from task2.weather import Weather


class FileUtility:

    @staticmethod
    def parse_files(dir_name):
        weathers = []
        if os.path.isdir(dir_name):
            content = os.listdir(dir_name)
            for name in content:
                if os.path.isfile(dir_name + name):
                    new_weather = Weather()
                    with open(dir_name + name) as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        for index, row in enumerate(csv_reader):
                            if index > 0:
                                new_reading = Reading(
                                    row[0],
                                    row[1],
                                    row[2],
                                    row[3],
                                    row[4],
                                    row[5],
                                    row[6],
                                    row[7],
                                    row[8],
                                    row[9],
                                    row[10],
                                    row[11],
                                    row[12],
                                    row[13],
                                    row[14],
                                    row[15],
                                    row[16],
                                    row[17],
                                    row[18],
                                    row[19],
                                    row[20],
                                    row[21],
                                    row[22],
                                )
                                new_weather.add_reading(new_reading)
                    weathers.append(new_weather)
        else:
            print(f"{dir_name} not a directory")
        return weathers
