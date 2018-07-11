from parser import parse_reading as psr
import fnmatch
import os
import csv


class WeatherRecord:
    def __init__(self,
                 date, max_temperature, mean_temperature, min_temperature, max_humidity, mean_humidity):
        self.date = date
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.mean_temperature = mean_temperature
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity


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
                    if row.get("PKT"):
                        date = psr(row["PKT"])
                    elif row.get("PKST"):
                        date = psr(row["PKST"])
                    weather_record = WeatherRecord(date,
                                                   psr(row["Max TemperatureC"]),
                                                   psr(row["Mean TemperatureC"]),
                                                   psr(row["Min TemperatureC"]),
                                                   psr(row["Max Humidity"]),
                                                   psr(row[" Mean Humidity"]))
                    if weather_record.max_humidity is not None:
                        self.readings.append(weather_record)
