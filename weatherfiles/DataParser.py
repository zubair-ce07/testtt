"""class to import data from files into data structure"""

import os
import csv


class DataParser:
    @staticmethod
    def parsefile(directory, data):
        """
        Read data from giles in directory one by one and place it in dictionary data
        :param directory: is path of the folder containing data files
        :param data: empty dictionary to be filled by method
        :return data: A dictionary with feature_names in "feature" and data in "values"
        """
        for file_name in os.listdir(directory):
            if '.txt' in file_name:
                file_path = os.path.join(directory, file_name)

                with open(file_path) as csvfile:
                    file_content = csv.reader(csvfile)
                    for row in file_content:
                        if not data['features']:
                            data['features'] = row
                        elif row != data['features'] and row[0] != 'PKST':
                            data['values'].append(row)

        # convert string values into relative data type on number
        for d in data['values']:
            for i in range(len(d)):
                try:
                    if '.' in d[i]:
                        d[i] = float(d[i])
                    else:
                        d[i] = int(d[i])
                except ValueError:
                    d[i] = d[i]

        return data
