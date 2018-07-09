from os import listdir
from os.path import isfile, join
import csv

import weather_day_reading


class WeatherReadingsReader:

    @staticmethod
    def read_day_reading(day):
        day = {k.strip(): v for k, v in day.items()}
        day_reading = weather_day_reading.WeatherReading(day)
        return day_reading

    @staticmethod
    def validate_day(day):
        day = {k.strip(): v for k, v in day.items()}
        if all(x for x in {k: day[k] for k in ('Mean TemperatureC', 'Min TemperatureC', 'Max TemperatureC',
                                               'Mean Humidity', 'Max Humidity', 'Min Humidity') if k in day}.values()):
            return True
        return False


    @staticmethod
    def read_file(path):
        weather_readings = []
        month_file = csv.DictReader(open(path))
        for row in month_file:
            if WeatherReadingsReader.validate_day(row):
                weather_readings.append(WeatherReadingsReader.read_day_reading(row))
        return weather_readings

    @staticmethod
    def get_weather_files(directory):
        return [f for f in listdir(directory) if isfile(join(directory, f))]

    @staticmethod
    def file_needs_to_be_read(file_name, year, month):
        if int(file_name.split('_')[2]) == year:
            if not month:
                return True
            elif file_name.split('_')[3].split('.')[0] == month:
                return True
        return False

    @staticmethod
    def read_readings(path, year, month=0):
        weather_readings = []
        file_names = WeatherReadingsReader.get_weather_files(path)
        for file_name in file_names:
            if WeatherReadingsReader.file_needs_to_be_read(file_name, year, month):
                    weather_readings += WeatherReadingsReader.read_file(path + file_name)
        return weather_readings
