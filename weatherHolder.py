""" This is the driver program for the weatherman task.


"""

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
        # print(len(files))
        for file in files:
            with open(directory + '/' + file) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                monthData = list(readCSV)
                header = monthData[0]
                del monthData[0]
                # print(header)
                # print(monthData)
                year = file[15:-8]
                month = file[20:-4] 
                print((year))
                print((month))

                if year not in self.data:
                    self.data[year] = {}

                if month not in self.data[year]:
                    self.data[year][month] = []

                for eachDay in monthData:
                    self.data[year][month].append(weatherReading(header, eachDay))
                    print(self.data[year][month][-1].weatherDataForTheDay)

                # for dayValue in monthData:
                #     # print(temp.weatherDataForTheDay)
                #     self.data[year][month].append(weatherReading(header, dayValue))
                #     print(self.data[year][month][-1].weatherDataForTheDay)
                    # (self.data[year][month]) = (yearDict[month])
                # for i in range(len(self.data[year][month])):
                #     print(self.data[year][month][i].weatherDataForTheDay)
                # break
        # print(len(self.data['2004']))
        # for year in self.data:
        #     for month in self.data[year]:
        #         print(year, month, len(self.data[year][month]))
                # print(len(self.data['2007']['Aug']))
                
    
    def get_month_data(self, year_month):
        year = year_month[:-4]
        month = year_month[5:]
        print(year)
        print(month)
        yearDict = self.data.get(year)
        if yearDict:
            return yearDict.get(month)
        else:
            return None

    def total_files(self):
        total_length = 0
        for year in self.data:
            total_length += len(self.data[year])

        return total_length

        