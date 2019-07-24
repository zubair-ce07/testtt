#!/usr/bin/python3
import calendar
import csv
import os
from datetime import datetime
from DataHolder import *


filenamePrefix = "Murree_weather_" #Murree_weather_2004_Aug
fileExtention = ".txt"

def getDailySelectedAttributes(record,fields):
    info = {}
    for field in fields:
        if not record[field]:
            return
        else:
            if (field == temperatureFields[0]):
                info[field] = datetime.strptime(record[temperatureFields[0]], "%Y-%m-%d")
            else:
                info[field] = int(record[field])
    return info


class DataReader:
    'Data reader class'

    def __init__(self, path):
        self.path = path

    def getMonthlyData(self,givenYear, monthNumber, selectedFields, command, highestTemp={}, minTemp={}, maxHumidity={}):
        givenMonth = calendar.month_name[int(monthNumber)][0:3]
        filePath = self.path + "/" + filenamePrefix + givenYear + "_" + givenMonth + fileExtention

        attributes = []
        monthlyRecords = []
        avgFields = [0,0,0]
        rowCount = 0;

        if (os.path.isfile(filePath)):
            with open(filePath) as dataFile:
                dictReader = csv.DictReader(dataFile)
                for row in dictReader:

                    dailyData = getDailySelectedAttributes(row,selectedFields)
                    if dailyData:
                        rowCount += 1;
                        monthlyRecords.append(dailyData)
                        if (command == "-e"):
                            if highestTemp:
                                if dailyData[selectedFields[2]] > highestTemp[selectedFields[2]]:
                                    highestTemp = dailyData
                            else:
                                highestTemp = dailyData

                            if minTemp:
                                if dailyData[selectedFields[1]] < minTemp[selectedFields[1]]:
                                    minTemp = dailyData
                            else:
                                minTemp = dailyData

                            if maxHumidity:
                                if dailyData[selectedFields[3]] > maxHumidity[selectedFields[3]]:
                                    maxHumidity = dailyData
                            else:
                                maxHumidity = dailyData
                        elif(command == "-a"):
                            avgFields[0] += dailyData[selectedFields[0]]
                            avgFields[1] += dailyData[selectedFields[1]]
                            avgFields[2] += dailyData[selectedFields[2]]


        if (command == "-c"):
            return monthlyRecords
        elif (command == "-e"):
            return [highestTemp,minTemp,maxHumidity]
        elif (command == "-a"):
            if (rowCount != 0):
                avgFields[0] /= rowCount
                avgFields[1] /= rowCount
                avgFields[2] /= rowCount
            return avgFields
