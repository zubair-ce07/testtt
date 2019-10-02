import csv
import re

from glob import glob

from temperatureResults import DayReading


class WeatherFilesParser:
    def parse_files(self, path, year):
        weather_readings = []
        weather_files = self.get_weather_files(path, year)
        for weather_file in weather_files:
            monthly_weather_file = open(weather_file)
            monthly_weather_file_reader = csv.DictReader(monthly_weather_file)
            for day_reading in monthly_weather_file_reader:
                if self.validate_weather_readings(day_reading):
                    weather_readings += [DayReading(day_reading)]
        return weather_readings

    def validate_weather_readings(self, day_reading):
        return all([day_reading['Max TemperatureC'], day_reading['Min TemperatureC'], day_reading['Max Humidity'],
                    day_reading[' Mean Humidity']])

    def get_weather_files(self, path, year):
        all_weather_files = glob(path + "/*")
        return self.get_required_files(all_weather_files, year)

    def get_required_files(self, all_weather_files, year):
        re_year = re.compile(str(year))
        return [file_name for file_name in all_weather_files if re_year.search(file_name)]
