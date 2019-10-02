import calendar
import csv
import re

from glob import glob
from temperatureResults import DayReading


class WeatherFilesParser:
    def parse_files(self, path, year):
        weather_readings = []
        weather_files = self.get_valid_files(path, year)
        if not weather_files:
            self.invalid_input(year)
        for weather_file in weather_files:
            temperature_file = open(weather_file)
            temperature_file_reader = csv.DictReader(temperature_file)
            for day_reading in temperature_file_reader:
                if self.validate_weather_readings(day_reading):
                    weather_readings += [DayReading(day_reading)]
        return weather_readings

    def validate_weather_readings(self, day_reading):
        if all([day_reading['Max TemperatureC'], day_reading['Min TemperatureC'], day_reading['Max Humidity'],
                day_reading[' Mean Humidity']]):
            return True
        return False

    def get_valid_files(self, path, year):
        if len(year.split('/')) > 1:
            re_year = re.compile(year.split('/')[0])
            re_month = re.compile(calendar.month_abbr[int(year.split('/')[1])])
            return [file_name for file_name in glob(path + "/*") if all([re_year.search(file_name),
                                                                              re_month.search(file_name)])]
        re_year = re.compile(year)
        return [file_name for file_name in glob(path + "/*") if re_year.search(file_name)]

    def invalid_input(self, year):
        print(f"No File for specified year/month {year}")
        print(f"please provide valid input")
        exit()
