"""This module read the weather files"""
import glob
import csv
from util import format_header, get_date_pattern


class File:
    """Open new file"""
    def __init__(self, name):
        self.open_new_file(name)

    def open_new_file(self, name):
        file = open(name)
        next(file)
        header = [format_header(h) for h in next(file).split(',')]
        self.__file = csv.DictReader(file, fieldnames=header)

    @property
    def file(self):
        return self.__file


class FileReader:
    """Open the weather file/files and read the records line by line"""

    def __init__(self, date, path):
        date_pattern = get_date_pattern(date)
        self.__files = glob.glob(f"{path}/*_weather_{date_pattern}.txt")
        self.__current_file_index = 0

    def has_next_file(self):
        """Check is next file is available"""
        return self.__current_file_index < len(self.__files)

    def get_next_filename(self):
        """Get next file name"""
        return self.__files[self.__current_file_index]

    def move_to_next_file(self):
        """Move index to next file"""
        self.__current_file_index += 1

    def records(self):
        """Yield data one by one for all the files"""
        while self.has_next_file():
            file = File(self.get_next_filename()).file
            for record in file:
                if record['max_temperaturec'] is not None:
                    yield record
            self.move_to_next_file()

        self.__current_file_index = 0
