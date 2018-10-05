#!/usr/bin/python3.6
import csv


class CsvFileDataHolder:
    def __init__(self):
        self.csv_file = dict()

    def add_new_attribute(self, attribute='', values=[]):
        self.csv_file[attribute] = values

    def get_attribute_values(self, attribute=''):
        key = [val for val in self.csv_file.keys() if attribute in val]
        values = self.csv_file.get(key[0])
        return values

    def get_int_converted_attribute_values(self, attribute=''):
        key = [val for val in self.csv_file.keys() if attribute in val]
        values = self.csv_file.get(key[0])
        converted_list = []
        for val in values:
            if val == None:
                converted_list.append(val)
            else:
                converted_list.append(int(val))
        return converted_list

    def display(self):
        for key, value in self.csv_file.items():
            print(key, value)

    def read_csv_file(self, file_path):
        try:
            with open(file_path) as csvfile:
                values = []
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    values.append(row)
            colom_iterator = 0
            while colom_iterator < len(values[0]):
                row_iterator = 1
                value = []
                while row_iterator < len(values):
                    if values[row_iterator][colom_iterator] == '':
                        value.append(None)
                    else:
                        value.append(values[row_iterator][colom_iterator])
                    row_iterator += 1
                    self.add_new_attribute(
                        values[0][colom_iterator], value
                    )
                del value
                colom_iterator += 1
        except IOError:
            self.csv_file = None
