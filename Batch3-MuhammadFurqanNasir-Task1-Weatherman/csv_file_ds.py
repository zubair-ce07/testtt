#!/usr/bin/python3.6


class Csv_file_ds:
    def __init__(self):
        self.csv_file = dict()

    def add_new_attribute(self, attribute = '', values = []):
        self.csv_file[attribute] = values

    def get_attribute_values(self, attribute = ''):
        key = [val for val in self.csv_file.keys() if attribute in val]
        values = self.csv_file.get(key[0])
        return values

    def get_int_converted_attribute_values(self, attribute = ''):
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