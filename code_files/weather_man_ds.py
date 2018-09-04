#!/usr/bin/python3.6
from csv_file_ds import Csv_file_ds


class Weather_man_ds:
    def __init__(self):
        self.year_holder = dict()

    def add_new_year(self, year='', months=[]):
        self.year_holder[year] = months

    def get_months_list_by_year(self, year):
        months = self.year_holder.get(year)
        return months
