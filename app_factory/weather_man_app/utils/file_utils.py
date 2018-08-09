# -*- coding: utf-8 -*-
"""
All communication with file system will be done through this script.
"""
import csv
import glob
import os

from app_factory.weather_man_app.utils.global_contants import FileGlobals, DateMapper


class ParseFiles(object):
    """
    Cass for parsing the weather files and populating the readings data structure with correct data types.
    """
    @staticmethod
    def parse_data(files_path, period):
        """
        Finds all files which come in a regex expression of year and/or month.
        :param files_path: Path from which file(s) can be assessed.
        :param period:
        :return:
        """
        file_patterns = glob.glob(os.path.join(files_path, '{file_prefix}_{year}_*{month}.{file_extention}'.format(
            file_prefix=FileGlobals.get('FILE_PREFIX'),
            year=period['year'],
            month=DateMapper.get_month_name(period['month']),
            file_extention=FileGlobals.get('FILE_EXTENTION')
        )))
        if not file_patterns:
            raise FileNotFoundError()
        for file in file_patterns:
            with open(file) as csv_file:
                yield csv.DictReader(csv_file)
