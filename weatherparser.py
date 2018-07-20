import os
import csv
import datetime

from containers import WeatherRecorder


class WeatherParser:

    def __init__(self):
        self.required_fields = ['Max TemperatureC', 'Min TemperatureC', 'Max Humidity', ' Mean Humidity']

    def parse(self, directory_path):
        weather_readings = []
        for f_name in os.listdir(directory_path):
            with open(os.path.join(directory_path, f_name), "r") as f_reader:
                for row in csv.DictReader(f_reader):
                    if all(row.get(key) for key in self.required_fields):
                        weather_readings.append(WeatherRecorder(
                                datetime.datetime.strptime(row.get('PKT', row.get('PKST')), '%Y-%m-%d'),
                                int(row.get('Max TemperatureC')), int(row.get('Min TemperatureC')),
                                int(row.get('Max Humidity')), int(row.get(' Mean Humidity'))
                            )
                        )
        return weather_readings
