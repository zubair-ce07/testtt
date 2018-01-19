# Module TO TAKE A FILE PATH AND POPULATE DATA

import csv
import glob
import os
import constants


class Populatedata:
    def __init__(self, year, month = "", filedir_path = ""):
        self.filedir_path = filedir_path
        self.year = year
        self.month = month
        self.datalist = []

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

    def printdatalist(self):
        count = 0
        if not self.datalist.__len__():
            print("no record for month of this year exist you provide")
        for data in self.datalist:
            print(data)
            if data[constants.CLOUD_COVER]:
                count += 1
        print(self.datalist.__len__(),count)