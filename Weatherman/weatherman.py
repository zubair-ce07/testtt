#!/usr/bin/python3
import sys
import os
import calendar
import csv

from datetime import datetime
import colorama
from colorama import Fore
from colorama import Style
from errors import *

temperatureFields = ["PKT", "Min TemperatureC", "Max TemperatureC"]
yearlyRecordFields = temperatureFields + ["Max Humidity"]
averageTemperatureFields = ["Min TemperatureC", "Max TemperatureC", " Mean Humidity"]

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

def getMonthlyData(givenYear, monthNumber, path, selectedFields, command, highestTemp={}, minTemp={}, maxHumidity={}):
    givenMonth = calendar.month_name[int(monthNumber)][0:3]
    filePath = path + "/" + filenamePrefix + givenYear + "_" + givenMonth + fileExtention

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


def main():
    if (len(sys.argv) < 2) or (len(sys.argv) % 2 == 1):
        raise InvalidArguments("Invalid arguments")


    path = sys.argv[1];
    if (not os.path.isdir(path)):
        raise InvalidArguments("Given folder does not exist");

    argIndex = 2

    for arg in range(2, len(sys.argv), 2):
        command = sys.argv[argIndex]
        commandArgument = sys.argv[argIndex + 1]
        if (command == '-e'):
            givenYear = commandArgument

            highestTemp = {}
            minTemp = {}
            maxHumidity = {}
            for monthNumber in range(1,13):

                facts = getMonthlyData(givenYear = givenYear,monthNumber = monthNumber,path = path,selectedFields = yearlyRecordFields,\
                command = command,highestTemp = highestTemp, minTemp = minTemp, maxHumidity = maxHumidity)

                highestTemp = facts[0]
                minTemp = facts[1]
                maxHumidity = facts[2]

            if (highestTemp):
                print("Highest:", end = " ")
                print(str(highestTemp[yearlyRecordFields[2]]) + "C on", end = " ")
                print(highestTemp[yearlyRecordFields[0]].strftime("%B %d"))

                print("Lowest:", end = " ")
                print(str(minTemp[yearlyRecordFields[1]]) + "C on", end = " ")
                print(minTemp[yearlyRecordFields[0]].strftime("%B %d"))

                print("Humidity:", end = " ")
                print(str(maxHumidity[yearlyRecordFields[3]]) + "% on", end = " ")
                print(maxHumidity[yearlyRecordFields[0]].strftime("%B %d"))
                print("\n")

            else:
                print("Data not found.\n")

        elif (command == '-a'):
            givenYear = commandArgument.split("/")[0]
            monthNumber = commandArgument.split("/")[1]

            avgFacts = getMonthlyData(givenYear = givenYear,monthNumber = monthNumber,path = path,\
                                            selectedFields = averageTemperatureFields,command = command)
            if (avgFacts[0] == 0 and avgFacts[1] == 0 and avgFacts[2] == 0):
                print(calendar.month_name[int(monthNumber)], givenYear)
                print("Data not found.\n")
            else:
                print("Highest Average: " + str(int(avgFacts[1])) + "C")
                print("Lowest Average: " + str(int(avgFacts[0])) + "C")
                print("Average Mean Humidity:" + str(int(avgFacts[2])) + "%\n")


        elif (command == '-c'):
            givenYear = commandArgument.split("/")[0]
            monthNumber = commandArgument.split("/")[1]

            monthlyRecords = getMonthlyData(givenYear = givenYear,monthNumber = monthNumber,path = path,\
                                            selectedFields = temperatureFields,command = command)

            #print(Fore.BLUE + "Hello World")
            print(calendar.month_name[int(monthNumber)], givenYear)
            if (monthlyRecords):

                for day in monthlyRecords:
                    print(day[temperatureFields[0]].strftime("%d"), end = " ")
                    print(Fore.BLUE + "+" * day[temperatureFields[1]], end = "")
                    print(Fore.RED + "+" * day[temperatureFields[2]], end = " ")
                    print(Fore.WHITE + str(day[temperatureFields[1]]) + "C - " + str(day[temperatureFields[2]]) + "C")
                print("\n")
            else:
                print("Data not found.\n")

        else:
            raise InvalidArguments("Invalid command: " + command);
        argIndex += 2;





if __name__ == "__main__":
    try:
        main()
    except InvalidArguments as error:
        print(error.message)
    '''except:
        print("Something went wrong")'''
