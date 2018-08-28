# -*- coding: utf-8 -*-
"""
All communication with file system will be done through this script.
"""
import csv
import glob
import os

from weather_man_app.utils.global_content import FileGlobalHandler, DateMapper


class FileParser:
    """
    Cass for parsing the weather files and populating the readings data structure with correct data types.
    """
    @staticmethod
    def parse_data(files_path, period):
        """
        Finds all files which come in a regex expression of year and/or month.
        :param files_path: Path from which file(s) can be assessed.
        :param period: year like 2010 or year/month 2010/1
        :return:
        """
        file_prefix = FileGlobalHandler.get_file_constant('FILE_PREFIX')
        month = DateMapper.get_month_name(period['month'])
        file_extention = FileGlobalHandler.get_file_constant('FILE_EXTENTION')
        year = period['year']
        file_patterns = glob.glob(os.path.join(files_path, f'{file_prefix}_{year}_*{month}.{file_extention}'))
        if not file_patterns:
            raise FileNotFoundError()
        for file in file_patterns:
            with open(file) as csv_file:
                yield csv.DictReader(csv_file)
