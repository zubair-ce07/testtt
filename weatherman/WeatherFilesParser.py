import csv
import re
from glob import glob

from temperatureResults import DayReading


class WeatherFilesParser:
    def parse_files(self, path, year):
        weather_readings = []
        weather_files = self.get_weather_files(path, year)
        for weather_file in weather_files:
            with open(weather_file, 'r') as monthly_weather_file:
                monthly_weather_file_reader = csv.DictReader(monthly_weather_file)
                for day_reading in monthly_weather_file_reader:
                    if self.validate_weather_readings(day_reading):
                        weather_readings += [DayReading(day_reading)]
        return weather_readings

    def validate_weather_readings(self, day_reading):
        return all([day_reading.get('Max TemperatureC'), day_reading.get('Min TemperatureC'),
                    day_reading.get('Max Humidity'), day_reading.get(' Mean Humidity')])

    def get_weather_files(self, path, year):
        re_year = re.compile(str(year))
        return [file_name for file_name in glob(path + "/*") if re_year.search(file_name)]

