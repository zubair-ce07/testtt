from os import listdir
from os.path import isfile, join
import csv

import WeatherData


class WeatherDataReader:

    @staticmethod
    def read_day(day):
        day = {k.strip(): v for k, v in day.items()}
        for index in ["Mean TemperatureC", "Min TemperatureC", "Max TemperatureC",
                      "Mean Humidity", "Max Humidity", "Min Humidity"]:
            if day[index] == '':
                day[index] = -100
            else:
                day[index] = int(day[index])
        try:
            date = day["PKT"].split('-')
        except:
            date = day["PKST"].split('-')
        day_data = WeatherData.WeatherData(int(date[0]), int(date[1]), int(date[2]), day["Max TemperatureC"],
                                           day["Min TemperatureC"], day["Mean TemperatureC"], day["Max Humidity"],
                                           day["Min Humidity"], day["Mean Humidity"])
        return day_data

    @staticmethod
    def read_file(path):
        list_month_data = []
        month_file = csv.DictReader(open(path))
        for row in month_file:
                list_month_data.append(WeatherDataReader.read_day(row))
        return list_month_data

    @staticmethod
    def read_yearly_data(path, year):
        weather_data = []
        files = [f for f in sorted(listdir(path)) if isfile(join(path, f))]
        for file_path in files:
            if int(file_path.split('_')[2]) == year:
                weather_data.append(WeatherDataReader.read_file(path + '/' + file_path))
        return weather_data

    @staticmethod
    def read_monthly_data(path, year, month):
        weather_data = []
        files = [f for f in sorted(listdir(path)) if isfile(join(path, f))]
        for file_path in files:
            if int(file_path.split('_')[2]) == year and file_path.split('_')[3].split('.')[0] == month:
                weather_data.append(WeatherDataReader.read_file(path + '/' + file_path))
        return weather_data
