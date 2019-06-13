import csv
from os import listdir
from os.path import isfile, join

class weatherHolder:
    data = {}
    def __init__(self, directory):
        files = [f for f in listdir(directory)]
        for file in files:
            print(file)
            with open(directory + '/' + file) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                # oneFile = list(readCSV)
                year = file[15:-8]
                month = file[20:-4] 
                # print(type(year))
                # print(type(month))
                self.data[year] = {}
                yearDict = self.data[year]
                yearDict[month] = list(readCSV)
                print(self.data)
        