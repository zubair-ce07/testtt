import os
import csv

from weather_data import WeatherData


class ParsingFiles:
    def __init__(self, path, argument_list):
        self.path = path
        self.argument_list = argument_list
        self.all_files_names = self.get_all_files_names()

    def get_all_files_names(self):
        return [file_name for file_name in os.listdir(self.path) for arg in self.argument_list if arg in file_name]

    def is_there_not_any_empty_element(self, myList):
        for element in myList:
            if element == '':
                return False
        return True

    def reading_files(self):
        all_weather_readings = WeatherData()

        for file_name in self.all_files_names:
            flag = True
            file_name_key = file_name.replace('.txt', '')
            all_weather_readings.max_temperature[file_name_key] = []
            all_weather_readings.min_temperature[file_name_key] = []
            all_weather_readings.max_humidity[file_name_key] = []
            all_weather_readings.mean_humidity[file_name_key] = []

            with open(''.join([self.path, file_name])) as file:
                file_reader = csv.DictReader(file)

                for line in file_reader:
                    if line:
                        if flag:
                            flag = False
                        else:
                            for value in line.values():
                                if len(value) > 1:
                                    line1 = [value[1], value[3], value[7], value[8]]
                                    if self.is_there_not_any_empty_element(line1):
                                        all_weather_readings.max_temperature[file_name_key].append(int(line1[0]))
                                        all_weather_readings.min_temperature[file_name_key].append(int(line1[1]))
                                        all_weather_readings.max_humidity[file_name_key].append(int(line1[2]))
                                        all_weather_readings.mean_humidity[file_name_key].append(float(line1[3]))

        return all_weather_readings
