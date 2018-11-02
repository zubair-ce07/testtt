#!/usr/bin/python3.6
from csv_file_data_holder import CsvFileDataHolder


class WeatherReadings:
    def __init__(self):
        self.weather_records = {}

    def add_new_year(self, year='', months=[]):
        self.weather_records[year] = months

    def months_data_of_year(self, year):
        return self.weather_records.get(year)
