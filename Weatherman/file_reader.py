"""This module read the weather files"""
import glob
import csv
from util import format_header, get_date_pattern


class File:
    """Open new file"""
    def __init__(self, name):
        self.next_record = None
        self.open_new_file(name)

    def open_new_file(self, name):
        """Open new file"""
        _file = open(name)
        next(_file)
        header = [format_header(h) for h in next(_file).split(',')]
        self.__file_pointer = csv.DictReader(_file, fieldnames=header)
        self.move_to_next_record()

    def move_to_next_record(self):
        self.next_record = next(self.__file_pointer)
        if self.next_record['max_temperaturec'] is None:
            self.next_record = None

    def peek(self):
        return self.next_record

    def records(self):
        """Read file record one by one"""
        if self.peek():
            record_to_send = self.peek()
            self.move_to_next_record()
            return record_to_send


class FileReader:
    """Open the weather file/files and read the records line by line"""

    def __init__(self, date, path):
        date_pattern = get_date_pattern(date)
        self.__files = glob.glob(f"{path}/*_weather_{date_pattern}.txt")
        self.__current_file_index = 0
        self._file = None

    def has_next_file(self):
        """Check is next file is available"""
        return self.__current_file_index < len(self.__files) -1

    def get_next_filename(self):
        """Get next file name"""
        return self.__files[self.__current_file_index]

    def move_to_next_file(self):
        """Move index to next file"""
        self.__current_file_index += 1

    def open_next_file(self):
        """Open next file"""
        self._file = File(self.get_next_filename())

    @property 
    def file(self):
        if self._file is None:
            self._file = File(self.get_next_filename())

        if self._file.peek() is None and self.has_next_file():
            self.move_to_next_file()
            self._file = File(self.get_next_filename())
        
        return self._file
