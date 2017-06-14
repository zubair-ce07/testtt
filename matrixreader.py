import calendar
import os
import fnmatch
import csv


class MatrixReader(object):

    STAR = '*'

    def __init__(self, dir, fixtures, columns):
        self._dir = dir
        self._columns = columns
        self._fixtures = fixtures

    def retrieve(self):
        result_set = []

        for file in self.list_files():
            with open(os.path.join(self._dir, file)) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    result_set.append([row[column] for column in reader.fieldnames
                                       if reader.fieldnames.index(column) in self._columns])
        return result_set


    def list_files(self):
        ls = []
        files = os.listdir(self._dir)

        for fix in self._fixtures:
            pattern = self.STAR + fix + self.STAR
            if not fix.isdigit():
                year, month = fix.split('/')
                pattern = self.STAR + year + '_' + calendar.month_abbr(month) + self.STAR
            for file in files:
                if fnmatch.fnmatch(file, pattern):
                    ls.append(file)
        return ls