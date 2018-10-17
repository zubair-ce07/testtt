"""
This Class read data from csv files into dictionary
"""
import os
import csv

from Analyzer import Analyzer


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
            for attribute_names, value in record.items():
                try:
                    record[attribute_names] = float(value)
                except ValueError:
                    pass

            if 'PKST' in record:
                record['PKT'] = Analyzer.parse_date(record['PKST'], '-')
            else:
                record['PKT'] = Analyzer.parse_date(record['PKT'], '-')

        return data
