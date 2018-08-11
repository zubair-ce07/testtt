"""
this module read data from csv file and return result
"""
import csv


class ReadCsv:
    """
    This class read the csv file and return result
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv_file(self):
        """
        this method read a csv file, create a list and return it
        :return:
        """
        with open(self.file_path) as csvfile:
            read_csv = csv.DictReader(csvfile, delimiter=',')
            file_data = list(read_csv)
        return file_data
