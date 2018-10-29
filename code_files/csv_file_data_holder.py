#!/usr/bin/python3.6
import csv
import datetime
import calendar


class CsvFileDataHolder:
    def __init__(self):
        self.data = dict()

    def months_name(self):
        key = [val for val in self.data.keys() if 'PK' in val]
        date_value = self.data.get(key[0])
        date = datetime.datetime.strptime(date_value[0], '%Y-%m-%d')
        return calendar.month_name[date.month]

    def add_new_attribute(self, attribute='', values=[]):
        self.data[attribute] = values

    def get_attribute_values(self, attribute=''):
        key = [val for val in self.data.keys() if attribute in val]
        values = self.data.get(key[0])
        return values

    def get_int_converted_attribute_values(self, attribute=''):
        key = [val for val in self.data.keys() if attribute in val]
        values = self.data.get(key[0])
        converted_list = []
        for val in values:
            if val == None:
                converted_list.append(val)
            else:
                converted_list.append(int(val))
        return converted_list

    def display(self):
        for key, value in self.data.items():
            print(key, value)

    def read_csv_file(self, file_path):
        try:
            with open(file_path) as csvfile:
                csv_reader = csv.DictReader(csvfile)
                headers = csv_reader.fieldnames
                for row in csv_reader:
                    for header in headers:
                        self.data.setdefault(header, []).append(
                            row.get(header) if row.get(header) else None)
        except IOError:
            self.data = None
