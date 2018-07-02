from os import listdir
from os.path import isfile, join
import csv

import WeatherData


class WeatherDataReader:

    @staticmethod
    def read_line(line):
        line = {k.strip(): v for k, v in line.items()}
        dayData = WeatherData.WeatherData()
        for index in ["Mean TemperatureC", "Min TemperatureC", "Max TemperatureC",
                      "Mean Humidity", "Max Humidity", "Min Humidity"]:
            if line[index] == '':
                line[index] = -100
            else:
                line[index] = int(line[index])
        try:
            date = line["PKT"].split('-')
        except:
            date = line["PKST"].split('-')
        dayData.year = int(date[0])
        dayData.month = int(date[1])
        dayData.day = int(date[2])
        dayData.highestT = line["Max TemperatureC"]
        dayData.meanT = line["Mean TemperatureC"]
        dayData.lowestT = line["Min TemperatureC"]
        dayData.highestH = line["Max Humidity"]
        dayData.meanH = line["Mean Humidity"]
        dayData.lowestH = line["Min Humidity"]
        return dayData

    @staticmethod
    def read_file(path):
        list_month_data = []
        month_file = csv.DictReader(open(path))
        for row in month_file:
                list_month_data.append(WeatherDataReader.read_line(row))
        return list_month_data

    @staticmethod
    def read(path):
        weather_data = []
        files = [f for f in sorted(listdir(path)) if isfile(join(path, f))]
        for file_path in files:
            weather_data.append(WeatherDataReader.read_file(path + '/' + file_path))
        return weather_data
