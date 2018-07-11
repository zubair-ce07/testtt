import datetime as dt
import fnmatch
import os
import csv


class WeatherRecord:
    def __init__(self, row):
        self.date = dt.datetime.strptime(row.get("PKT") or row.get("PKST"), "%Y-%m-%d")
        self.max_temperature = int(row.get("Max TemperatureC")) if row.get("Max TemperatureC") else None
        self.mean_temperature = int(row.get("Mean TemperatureC")) if row.get("Mean TemperatureC") else None
        self.min_temperature = int(row.get("Min TemperatureC")) if row.get("Min TemperatureC") else None
        self.max_humidity = int(row.get("Max Humidity")) if row.get("Max Humidity") else None
        self.mean_humidity = int(row.get(" Mean Humidity")) if row.get(" Mean Humidity") else None


class WeatherRegister:
    def __init__(self):
        self.month = None
        self.year = None
        self.readings = list()

    def read_dir(self, directory_path, year, month='*'):
        self.month = month
        self.year = year
        files = os.listdir(directory_path)
        for filename in fnmatch.filter(files, f"Murree_weather_{year}_{month[:3]}.txt"):
            with open(directory_path+filename, newline='\n') as file:
                for row in csv.DictReader(file):
                    self.readings.append(WeatherRecord(row))
