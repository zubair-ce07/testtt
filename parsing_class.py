import os
import csv

from weather_data import WeatherData


class ParsingFiles:
    def __init__(self, path, flag, query):
        self.path = path
        self.flag = flag
        self.query = query
        self.months = {
            '1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun',
            '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
        }
        self.all_files_names = self.get_all_files_names()

    def get_all_files_names(self):
        files = os.listdir(self.path)
        if self.flag == '-e':
            new_files = [file for file in files if self.query in file]
            return new_files

        if self.flag == '-a' or self.flag == '-c':
            year_month = self.query.split('/')
            year_plus_month = "{}_{}".format(year_month[0], self.months[str(int(year_month[1]))])
            new_files = [file for file in files if year_plus_month in file]
            return new_files


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
                file_reader = csv.reader(file)

                for line in file_reader:
                    if len(line) > 1:
                        if flag:
                            flag = False
                        else:
                            line = [line[1], line[3], line[7], line[8]]
                            if self.is_there_not_any_empty_element(line):
                                all_weather_readings.max_temperature[file_name_key].append(int(line[0]))
                                all_weather_readings.min_temperature[file_name_key].append(int(line[1]))
                                all_weather_readings.max_humidity[file_name_key].append(int(line[2]))
                                all_weather_readings.mean_humidity[file_name_key].append(float(line[3]))

        return all_weather_readings
