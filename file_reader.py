"""This module read the weather files"""
import glob
import csv
from util import format_header, get_date_pattern


class File:
    """Open new file"""
    def __init__(self, name):
        self.open_new_file(name)

    def open_new_file(self, name):
        _file = open(name)
        next(_file)
        header = [format_header(h) for h in next(_file).split(',')]
        self.__file_pointer = csv.DictReader(_file, fieldnames=header)

    def records(self):
        """Read file record one by one"""
        for record in self.__file_pointer:
            if record['max_temperaturec'] is not None:
                yield record


class FileReader:
    """Open the weather file/files and read the records line by line"""

    def __init__(self, date, path):
        date_pattern = get_date_pattern(date)
        self.__files = glob.glob(f"{path}/*_weather_{date_pattern}.txt")
        self.__current_file_index = 0
        self._file = None

    def has_next_file(self):
        """Check is next file is available"""
        return self.__current_file_index < len(self.__files)

    def get_next_filename(self):
        """Get next file name"""
        return self.__files[self.__current_file_index]

    def move_to_next_file(self):
        """Move index to next file"""
        self.__current_file_index += 1

    def open_next_file(self):
        self._file = File(self.get_next_filename())

    def records(self):
        """Yield data one by one for all the files"""
        while self.has_next_file():
            self.open_next_file()
            for record in self._file.records():
                yield record
            self.move_to_next_file()

        self.__current_file_index = 0
