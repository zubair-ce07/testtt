"""This module read the weather files
"""
from datetime import timedelta
from util import strip_list, parse_date
import constants

class FileReader:
    """Open the weather file/files and read the records line by line
    """
    def __init__(self, date, path):
        self.__date, self.__read_type, self.__end_date = parse_date(date)
        self.__path = path
        self.__file_pointer = None
        self.keys = []
        self.values = []
        self.initialize()

    def initialize(self):
        """Open file of the year and month
        """
        year = self.__date.strftime('%Y')
        month = self.__date.strftime('%b')
        filepath = f"{self.__path}/{constants.CITY}_weather_{year}_{month}.txt"
        self.__file_pointer = open(filepath, 'r')
        self.__file_pointer.readline()
        
        self.set_keys()

    def set_keys(self):
        """Set keys 
        """
        self.keys = self.__file_pointer.readline().split(",")
        strip_list(self.keys)

    def set_values(self):
        """Set values 
        """
        next_line = self.__file_pointer.readline()
        if not next_line or len(next_line.split(",")) != 23:
            self.values = []
        else:
            self.values = next_line.split(",")
            strip_list(self.values)

    def next_record(self):
        """Read records line by line from the file.
        Call Recursively in order to read the new month file

        return a dictionary containg keys and values of the current record
        """

        self.set_values()
        if self.values == []:
            if self.__read_type == "Month":
                return None
            if self.__date < self.__end_date:
                self.__date += timedelta(days=31)
                self.initialize()
                self.next_record()

        return dict(zip(self.keys, self.values))
