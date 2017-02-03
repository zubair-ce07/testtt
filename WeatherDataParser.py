import weatherman_util
from WeatherData import WeatherData
from functools import reduce
import csv


class WeatherDataParser(object):
    
    def __init__(self, directory):
        self.directory = directory
        self.data = []

    def parse_data(self):
        files = weatherman_util.get_files(self.directory)
        weather_objects = []
        for file in files:
            with open(file) as f:
                reader = csv.DictReader(f, skipinitialspace=True)
                objs = list(map(lambda row: map_to_weather_obj(row), reader))
                weather_objects.append(objs)

        self.data = reduce(list.__add__, weather_objects)

    def get_data(self):
        return self.data


def map_to_weather_obj(row):
    date = row.get('PKT') or row.get('PKST')
    
    return WeatherData(date=date,
                       max_temp=row['Max TemperatureC'],
                       mean_temp=row['Mean TemperatureC'],
                       min_temp=row['Min TemperatureC'],
                       max_humidity=row['Max Humidity'],
                       mean_humidity=row['Mean Humidity'],
                       min_humidity=row['Min Humidity'])
