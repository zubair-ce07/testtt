from os import listdir
from os.path import isfile, join
import csv

import weather_day_reading


class WeatherReadingsReader:

    @staticmethod
    def read_day(day):
        day = {k.strip(): v for k, v in day.items()}
        day_reading = weather_day_reading.WeatherReading(day)
        return day_reading

    @staticmethod
    def validate_day(day):
        day = {k.strip(): v for k, v in day.items()}
        for index in ['Mean TemperatureC', 'Min TemperatureC', 'Max TemperatureC',
                      'Mean Humidity', 'Max Humidity', 'Min Humidity']:
            if day[index] == '':
                return False
        return True

    @staticmethod
    def read_file(path):
        weather_readings = []
        month_file = csv.DictReader(open(path))
        for row in month_file:
            if WeatherReadingsReader.validate_day(row):
                weather_readings.append(WeatherReadingsReader.read_day(row))
        return weather_readings

    @staticmethod
    def read_readings(path, year, month=0):
        weather_readings = []
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file_name in files:
            if month != 0:
                if int(file_name.split('_')[2]) == year and file_name.split('_')[3].split('.')[0] == month:
                    weather_readings += WeatherReadingsReader.read_file(path + file_name)
            else:
                if int(file_name.split('_')[2]) == year:
                    weather_readings += WeatherReadingsReader.read_file(path + file_name)
        return weather_readings
