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

    def next_record(self):
        """Open the file if file_pointer is none. Read records line by line from the file.
        Call recursively in case of read type Year to open every month file.

        return a dictionary containg keys and values of the current record
        """
        if self.__file_pointer is None:
            year = self.__date.strftime('%Y')
            month = self.__date.strftime('%b')
            filepath = f"{self.__path}/{constants.CITY}_weather_{year}_{month}.txt"
            self.__file_pointer = open(filepath, 'r')
            self.__file_pointer.readline()
            self.keys = self.__file_pointer.readline().split(",")
            strip_list(self.keys)
            self.values = self.__file_pointer.readline().split(",")
            strip_list(self.values)
            return dict(zip(self.keys, self.values))

        next_line = self.__file_pointer.readline()
        if not next_line or len(next_line.split(",")) is not 23:
            if self.__read_type is "Month":
                return None

            if self.__date < self.__end_date:
                self.__date += timedelta(days=31)
                self.__file_pointer = None
                return self.next_record()

        self.values = next_line.split(",")
        strip_list(self.values)
        return dict(zip(self.keys, self.values))
