# Module TO TAKE A FILE PATH AND POPULATE DATA

import csv
import glob
import os
import constants


class Populatedata:
    """class take file directory path year and month(option)
    and populate data form the file directory form
    the files according to specified year"""

    def __init__(self, filedir_path, year, month = ""):
        self.filedir_path = filedir_path
        self.year = year
        self.month = month
        self.datalist = []

    # method to populate data from files
    def populatedata(self):
        for filename in glob.glob(
                os.path.join(
                    self.filedir_path,
                    '*{}*{}.txt'.format(self.year, self.month)
                )):
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.datalist.append(row)
