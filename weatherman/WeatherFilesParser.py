import csv
import re
from glob import glob

from temperatureResults import DayReading


class WeatherFilesParser:
    def parse_files(self, path, year):
        weather_records = []
        weather_files = self.get_weather_files(path, year)
        for weather_file in weather_files:
            with open(weather_file, 'r') as weather_readings:
                reader = csv.DictReader(weather_readings)
                for single_record in reader:
                    if self.validate_weather_readings(single_record):
                        weather_records += [DayReading(single_record)]
        return weather_records

    def validate_weather_readings(self, single_record):
        return all([single_record.get('Max TemperatureC'), single_record.get('Min TemperatureC'),
                    single_record.get('Max Humidity'), single_record.get(' Mean Humidity')])

    def get_weather_files(self, path, year):
        re_year = re.compile(str(year))
        return [file_name for file_name in glob(path + "/*") if re_year.search(file_name)]

