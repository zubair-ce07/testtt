import csv
from os import listdir
from os.path import isfile, join

class weatherReading:
    weatherDataForTheDay = {}
    def __init__(self, header, oneReading):
        for attribute, value in zip(header, oneReading):
            self.weatherDataForTheDay[attribute.strip()] = value
        

class weatherHolder:
    data = {}
    def __init__(self, directory):
        files = [f for f in listdir(directory)]
        print(len(files))
        for file in files:
            with open(directory + '/' + file) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                monthData = list(readCSV)
                header = monthData[0]
                del monthData[0]
                year = file[15:-8]
                month = file[20:-4] 
                # print(type(year))
                # print(type(month))
                if year not in self.data:
                    self.data[year] = {}
                yearDict = self.data[year]
                if month not in yearDict:
                    yearDict[month] = []
                for dayValue in monthData:
                    temp = weatherReading(header, dayValue)
                    yearDict[month].append(temp)
        # print(len(self.data['2004']))
        for year in self.data:
            for month in self.data[year]:
                print(year, month, len(self.data[year][month]))
                # print(len(self.data['2007']['Aug']))
                
    
    def get_month_data(self, year_month):
        print(year_month[:-4])
        print(year_month[5:])
        yearDict = self.data[year_month[:-4]]
        return yearDict[year_month[5:]]

    def total_files(self):
        total_length = 0
        for year in self.data:
            total_length += len(self.data[year])

        return total_length

        