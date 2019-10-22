"""This module read the weather files"""
import glob
import csv
from util import format_header, get_date_pattern

class FileReader:
    """Open the weather file/files and read the records line by line"""
    def __init__(self, date, path):
        date_pattern = get_date_pattern(date)
        self.__path = path
        self.__files = glob.glob(f"{path}/*_weather_{date_pattern}.txt")
        self.__current_file_index = 0
        self.__file_pointer = None
        self.keys = []
        self.values = []
        self.initialize()

    def initialize(self):
        """Open file of the year and month"""
        file = open(self.get_next_filename())
        next(file)
        header = [format_header(h) for h in next(file).split(',')]
        self.__file_pointer = csv.DictReader(file, fieldnames=header)

    def has_next_file(self):
        """Check is next file is available"""
        return  self.__current_file_index < len(self.__files) -1

    def get_next_filename(self):
        """Get next file name"""
        return self.__files[self.__current_file_index]

    def move_to_next_file(self):
        """Move index to next file"""
        self.__current_file_index += 1

    def next_record(self):
        """Read records line by line from the file.
        Call Recursively in order to read the new month file

        return a dictionary containg keys and values of the current record
        """
        next_record = next(self.__file_pointer)
        if next_record['max_temperaturec'] is not None:
            return next_record

        if self.has_next_file():
            self.move_to_next_file()
            self.initialize()
            return self.next_record()
        return None
