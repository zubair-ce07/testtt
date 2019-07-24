#!/usr/bin/python3
import sys
import os

from errors import *
from DataReader import *
from Reports import *


def validateArguments(args):
    if (len(args) < 2) or (len(args) % 2 == 1):
        raise InvalidArguments("Invalid arguments")

    path = args[1];
    if (not os.path.isdir(path)):
        raise InvalidArguments("Given folder does not exist");
    return path


def main():

    path = validateArguments(sys.argv)
    reader = DataReader(path)
    reports = DataReport()

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

                facts = reader.getMonthlyData(givenYear = givenYear,monthNumber = monthNumber,selectedFields = yearlyRecordFields,\
                                                command = command,highestTemp = highestTemp, minTemp = minTemp, maxHumidity = maxHumidity)
                highestTemp = facts[0]
                minTemp = facts[1]
                maxHumidity = facts[2]
            reports.printYearlyReport(facts)


        elif (command == '-a'):
            givenYear = commandArgument.split("/")[0]
            monthNumber = commandArgument.split("/")[1]

            avgFacts = reader.getMonthlyData(givenYear = givenYear,monthNumber = monthNumber,selectedFields = averageTemperatureFields\
                                            ,command = command)
            reports.printAverageReport(avgFacts, monthNumber, givenYear)


        elif (command == '-c'):
            givenYear = commandArgument.split("/")[0]
            monthNumber = commandArgument.split("/")[1]

            monthlyRecords = reader.getMonthlyData(givenYear = givenYear,monthNumber = monthNumber,selectedFields = temperatureFields\
                                            ,command = command)
            reports.printMonthlyReport(monthlyRecords, monthNumber, givenYear)

        else:
            raise InvalidArguments("Invalid command: " + command);

        argIndex += 2;


if __name__ == "__main__":
    try:
        main()
    except InvalidArguments as error:
        print(error.message)
    except:
        print("Something went wrong")
