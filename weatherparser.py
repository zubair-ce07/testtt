import os.path
import csv
import calendar
from collections import namedtuple


WeatherRecord = namedtuple('Weather', ('date, max_temp, min_temp, max_humidity, mean_humidity'))


class WeatherParser:

    weather_fields = ['Max TemperatureC', 'Min TemperatureC', 'Max Humidity', ' Mean Humidity']

    def generate_filenames(self, date, directory):
        def filepath(directory, year, month):
            return f'{directory}/Murree_weather_{year}_{calendar.month_abbr[int(month)]}.txt'
        weather_date = date.split("/")
        if len(weather_date) > 1:
            return [filepath(directory, weather_date[0], weather_date[1])]
        return [filepath(directory, weather_date[0], month) for month in range(12)]

    def read_weather_file(self, date, directory):
        weather_readings = []
        filenames = self.generate_filenames(date, directory)
        for weather_file in filenames:
            if not os.path.exists(weather_file):
                continue
            with open(weather_file) as weatherfile:
                reader = csv.DictReader(weatherfile)
                for row in reader:
                    if not all(row.get(fields) for fields in self.weather_fields):
                        continue
                    weather_readings += [WeatherRecord(row.get('PKT') or row.get('PKST'),
                                        int(row['Max TemperatureC']), int(row['Min TemperatureC']),
                                        int(row['Max Humidity']), int(row[' Mean Humidity']))]
        return weather_readings
