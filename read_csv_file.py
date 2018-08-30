#!/usr/bin/python3.6

import csv

from csv_file_ds import Csv_file_ds

def read_csv_file(file_path):
    month = Csv_file_ds()
    try:
        with open(file_path) as csvfile:
            values = []
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                values.append(row)
        colom_iterator=0
        while colom_iterator < len(values[0]):
            row_iterator = 1
            value = []
            while row_iterator < len(values):
                if values[row_iterator][colom_iterator] == '':
                    value.append(None)
                else:
                    value.append(values[row_iterator][colom_iterator])
                row_iterator+=1
            month.add_new_attribute(values[0][colom_iterator], value)
            del value
            colom_iterator+=1
    except IOError:
        return None
    return month