#!/usr/bin/python3.6
import csv
import datetime
import calendar


class CsvFileDataHolder:
    def __init__(self):
        self.csv_file_data = dict()

    def months_name(self):
        date_header = [header_value for header_value in self.csv_file_data.keys()
                       if 'PK' in header_value]
        date_value = self.csv_file_data.get(date_header[0])
        date = datetime.datetime.strptime(date_value[0], '%Y-%m-%d')
        return calendar.month_name[date.month]

    def add_new_attribute(self, header, values):
        self.csv_file_data[header] = values

    def attribute_values(self, header):
        headers = [header_value for header_value in self.csv_file_data.keys()
                  if header in header_value]
        return [int(value) if value else None for value in self.csv_file_data.get(headers[0])]

    def read_csv_file(self, file_path):
        try:
            with open(file_path, 'r') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                headers = csv_reader.fieldnames

                for row in csv_reader:
                    for header in headers:
                        self.csv_file_data.setdefault(header, []).append(row.get(header))

        except IOError:
            self.csv_file_data = None
