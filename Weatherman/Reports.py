#!/usr/bin/python3
import calendar
import colorama
from colorama import Fore
from colorama import Style

from DataHolder import *


class DataReport:
    'Class to print reports'

    def printYearlyReport(self, facts):

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

    def printAverageReport(self, avgFacts, monthNumber, givenYear):
        if (avgFacts[0] == 0 and avgFacts[1] == 0 and avgFacts[2] == 0):
            print(calendar.month_name[int(monthNumber)], givenYear)
            print("Data not found.\n")
        else:
            print("Highest Average: " + str(int(avgFacts[1])) + "C")
            print("Lowest Average: " + str(int(avgFacts[0])) + "C")
            print("Average Mean Humidity:" + str(int(avgFacts[2])) + "%\n")

    def printMonthlyReport(self, monthlyRecords, monthNumber, givenYear):
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
