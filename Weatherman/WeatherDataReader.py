from os import listdir
from os.path import isfile, join
import csv

import WeatherData


class WeatherDataReader:

    @staticmethod
    def read_day(day):
        day = {k.strip(): v for k, v in day.items()}
        day_data = WeatherData.WeatherReading(day)
        return day_data

    @staticmethod
    def validate_day(day):
        day = {k.strip(): v for k, v in day.items()}
        for index in ["Mean TemperatureC", "Min TemperatureC", "Max TemperatureC",
                      "Mean Humidity", "Max Humidity", "Min Humidity"]:
            if day[index] == '':
                return False
        return True

    @staticmethod
    def read_file(path):
        list_month_data = []
        month_file = csv.DictReader(open(path))
        for row in month_file:
            if WeatherDataReader.validate_day(row):
                list_month_data.append(WeatherDataReader.read_day(row))
        return list_month_data

    @staticmethod
    def read_yearly_data(path, year):
        weather_data = []
        files = [f for f in sorted(listdir(path)) if isfile(join(path, f))]
        for file_path in files:
            if int(file_path.split('_')[2]) == year:
                weather_data = weather_data + WeatherDataReader.read_file(path + '/' + file_path)
        return weather_data

    @staticmethod
    def read_monthly_data(path, year, month):
        weather_data = []
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file_name in files:
            if int(file_name.split('_')[2]) == year and file_name.split('_')[3].split('.')[0] == month:
                weather_data = weather_data + WeatherDataReader.read_file(path + '/' + file_name)
        return weather_data
