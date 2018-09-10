"""
This Class read data from csv files into dictionary
"""
import os
import csv


class DataReader:
    @staticmethod
    def parsefile(directory):
        """
        Read data from files in directory one by one and place it in dictionary data
        :param directory: is path of the folder containing data files
        :return data: A list of dictionaries where each dictionary represent a record
        """
        data = []
        for file_name in os.listdir(directory):
            if '.txt' in file_name:
                file_path = os.path.join(directory, file_name)
                with open(file_path) as csvfile:
                    data.extend(list(csv.DictReader(csvfile)))

        for record in data:
            for key, value in record.items():
                try:
                    record[key] = float(record[key]) if record[key] and '.' in record[key] else int(record[key])
                except ValueError:
                    record[key] = record[key]
            if 'PKT' not in record:
                record['PKT'] = record['PKST']
                del record['PKST']

        return data
