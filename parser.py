# -*- coding: utf-8 -*-
import argparse
import csv
import os

import enum


class Report(enum.IntEnum):
    annual = 1
    hottestDay = 2
    coldestDay = 3
    yellow = 4


KEY_YEAR = "year"
KEY_DATE = "date"
KEY_TEMP = "temp"

KEY_MAX_TEMPERATURE = "Max TemperatureC"
KEY_MIN_TEMPERATURE = "Min TemperatureC"
KEY_MAX_HUMIDITY = "Max Humidity"
KEY_MIN_HUMIDITY = "Min Humidity"

KEY_ANNUAL_DATA = "Yearly Data"
KEY_HOTTEST_DAY_DATA = "Hottest Data"
KEY_COLDEST_DAY_DATA = "Coldest Data"


def annual_report(data):
    print "Year\tMAX Temp\tMIN Temp\tMAX Humidity\tMIN​ Humidity​"
    print "--------------------------------------------------------------------------"
    for key in data:
        year = data[key]
        result = "{} \t\t {} \t\t {} \t\t {} \t\t {}".format(key, year[KEY_MAX_TEMPERATURE], year[KEY_MIN_TEMPERATURE],
                                                             year[KEY_MAX_HUMIDITY], year[KEY_MIN_HUMIDITY])
        print result


def hottest_report(data):
    print "Year\t Date\tTemp"
    print "--------------------"
    for key in data:
        year = data[key]
        result = "{} \t {} \t {}".format(key, year[KEY_DATE], year[KEY_TEMP])
        print result


def coldest_report(data):
    print "Year\t Date\tTemp"
    print "--------------------"
    for key in data:
        year = data[key]
        result = "{} \t {} \t {}".format(key, year[KEY_DATE], year[KEY_TEMP])
        print result


def analyse_data(data_dir):
    titles = ""
    currentDate = ""
    yearlyData = dict()
    hottestDayData = dict()
    coldestDayData = dict()
    weatherFiles = os.listdir(data_dir)
    if not len(weatherFiles):
        print "data directory is empty"
        return
    for weatherFile in weatherFiles:
        monthFileName = os.path.abspath(os.path.join(data_dir, weatherFile))
        with open(monthFileName, 'r') as monthlyFile:
            csv_f = csv.reader(monthlyFile)
            titles = []
            for index, row in enumerate(csv_f):
                if not index:
                    continue
                if index == 1:
                    for item in row:
                        titles.append(item)
                    continue
                dayData = dict()
                if not row[0].__contains__("<!--"):
                    parsedDayList = row
                    for index, title in enumerate(titles):
                        dayData[str.strip(title)] = parsedDayList[index]
                    currentDate = str(dayData.get('PKT') or dayData.get('PKST'))
                    selectedYear = int(currentDate.split("-").__getitem__(0))
                    if selectedYear not in yearlyData:
                        yearData = dict()
                        yearData[KEY_MAX_TEMPERATURE] = -99
                        yearData[KEY_MIN_TEMPERATURE] = 99
                        yearData[KEY_MAX_HUMIDITY] = -99
                        yearData[KEY_MIN_HUMIDITY] = 99
                        yearlyData[selectedYear] = yearData

                        hottestDay = dict()
                        hottestDay[KEY_DATE] = ""
                        hottestDay[KEY_TEMP] = -99
                        hottestDayData[selectedYear] = hottestDay

                        coldestDay = dict()
                        coldestDay[KEY_DATE] = ""
                        coldestDay[KEY_TEMP] = -99
                        coldestDayData[selectedYear] = coldestDay
                    if dayData[KEY_MAX_TEMPERATURE]:
                        if yearlyData[selectedYear][KEY_MAX_TEMPERATURE] < int(dayData[KEY_MAX_TEMPERATURE]):
                            yearlyData[selectedYear][KEY_MAX_TEMPERATURE] = int(dayData[KEY_MAX_TEMPERATURE])
                            hottestDayData[selectedYear][KEY_TEMP] = int(dayData[KEY_MAX_TEMPERATURE])
                            hottestDayData[selectedYear][KEY_DATE] = currentDate
                    if dayData[KEY_MIN_TEMPERATURE]:
                        if yearlyData[selectedYear][KEY_MIN_TEMPERATURE] > int(dayData[KEY_MIN_TEMPERATURE]):
                            yearlyData[selectedYear][KEY_MIN_TEMPERATURE] = int(dayData[KEY_MIN_TEMPERATURE])
                            coldestDayData[selectedYear][KEY_TEMP] = int(dayData[KEY_MIN_TEMPERATURE])
                            coldestDayData[selectedYear][KEY_DATE] = currentDate
                    if dayData[KEY_MAX_HUMIDITY]:
                        if yearlyData[selectedYear][KEY_MAX_HUMIDITY] < int(dayData[KEY_MAX_HUMIDITY]):
                            yearlyData[selectedYear][KEY_MAX_HUMIDITY] = int(dayData[KEY_MAX_HUMIDITY])
                    if dayData[KEY_MIN_HUMIDITY]:
                        if yearlyData[selectedYear][KEY_MIN_HUMIDITY] > int(dayData[KEY_MIN_HUMIDITY]):
                            yearlyData[selectedYear][KEY_MIN_HUMIDITY] = int(dayData[KEY_MIN_HUMIDITY])
    return {KEY_ANNUAL_DATA: yearlyData, KEY_HOTTEST_DAY_DATA: hottestDayData, KEY_COLDEST_DAY_DATA: coldestDayData}


def main():
    print "**********WEATHERMAN**********"

    analysedData = dict()
    dataDirectory = ""
    reportNumber = Report.annual

    argumentParser = argparse.ArgumentParser(prog='Weatherman')
    argumentParser.add_argument('-d', '--dir', help='Data Directory')  # optional
    argumentParser.add_argument('-r', '--report', help='Report Number', type=int)  # positional
    arguments = argumentParser.parse_args()
    if arguments.dir:
        if not os.path.dirname(arguments.dir):
            print "Please provide correct data directory path"
            return
        else:
            dataDirectory = arguments.dir
    else:
        argumentParser.print_help()
        return
    if arguments.report:
        reportNumber = arguments.report

    analysedData = analyse_data(dataDirectory)

    if reportNumber == Report.annual:
        annual_report(analysedData[KEY_ANNUAL_DATA])
    if reportNumber == Report.hottestDay:
        hottest_report(analysedData[KEY_HOTTEST_DAY_DATA])
    if reportNumber == Report.coldestDay:
        coldest_report(analysedData[KEY_COLDEST_DAY_DATA])


if __name__ == '__main__':
    main()
