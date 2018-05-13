import os.path
import csv
import calendar
from collections import namedtuple


class WeatherParser:

    weatherRecord = namedtuple('Weather', ('date, max_temp, min_temp, max_humidity, mean_humidity'))
    weather_fields = ['Max TemperatureC', 'Min TemperatureC', 'Max Humidity', ' Mean Humidity']

    def generate_filename(self, date, directory):
        weather_date = date.split("/")
        if len(weather_date) > 1:
            return [f'{directory}/Murree_weather_{weather_date[0]}_{calendar.month_abbr[int(weather_date[1])]}.txt']
        return [f'{directory}/Murree_weather_{weather_date[0]}_{calendar.month_abbr[int(months_count)]}.txt' \
                for months_count in range(12)]

    def read_weather_file(self, date, directory):
        weather_readings = []
        filenames = self.generate_filename(date, directory)
        for weather_file in filenames:
            if not os.path.exists(weather_file):
                continue
            with open(weather_file) as weatherfile:
                reader = csv.DictReader(weatherfile)
                for row in reader:
                    if not all(row.get(fields) for fields in self.weather_fields):
                        pass
                    weather_readings += [self.weatherRecord(row.get('PKT') or row.get('PKST'),
                                        int(row['Max TemperatureC']), int(row['Min TemperatureC']),
                                        int(row['Max Humidity']), int(row[' Mean Humidity']))]
        return weather_readings
