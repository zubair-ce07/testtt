import csv
import glob
import os

from weatherman_repo.utils.globals import FileGlobals


class ParseFiles(object):
    """
    Cass for parsing the weather files and populating the readings data structure with correct data types.
    """
    @staticmethod
    def parse_data(file_path, year, month):
        file_patterns = glob.glob(os.path.join(file_path, '{file_prefix}_{year}_*{month}.{file_extention}'.format(
            file_prefix=FileGlobals.get('FILE_PREFIX'),
            year=year,
            month=month,
            file_extention=FileGlobals.get('FILE_EXTENTION')
        )))
        for file in file_patterns:
            with open(file) as csv_file:
                yield csv.DictReader(csv_file)
