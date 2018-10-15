#!/usr/bin/python3.6
from csv_file_data_holder import CsvFileDataHolder


class WeatherReadings:
    def __init__(self):
        self.year_holder = dict()

    def add_new_year(self, year='', months=[]):
        self.year_holder[year] = months

    def get_months_data_of_year(self, year):
        months = self.year_holder.get(year)
        return months
