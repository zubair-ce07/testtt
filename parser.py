# -*- coding: utf-8 -*-
import argparse
import csv
import os

KEY_YEAR = "year"
KEY_DATE = "date"
KEY_TEMP = "temp"

KEY_MAX_TEMP = "Max TemperatureC"
KEY_MIN_TEMP = "Min TemperatureC"
KEY_MAX_HUMD = "Max Humidity"
KEY_MIN_HUMD = "Min Humidity"

KEY_ANNUAL_DATA = "Yearly Data"
KEY_HOTTEST_DAY_DATA = "Hottest Data"
KEY_COLDEST_DAY_DATA = "Coldest Data"

ANNUAL_REPORT = 1
HOTTEST_DAY_REPORT = 2
COLDEST_DAY_REPORT = 3


def annual_report(data):
    print "Year\tMAX Temp\tMIN Temp\tMAX Humidity\tMIN​ Humidity​"
    print "--------------------------------------------------------------------------"
    for key in data:
        year = data[key]
        print key, "\t\t", str(year[KEY_MAX_TEMP]), "\t\t", str(year[KEY_MIN_TEMP]), "\t\t" \
            , str(year[KEY_MAX_HUMD]), "\t\t", str(year[KEY_MIN_HUMD])


def hottest_report(data):
    print "Year\t Date\tTemp"
    print "--------------------"
    for key in data:
        year = data[key]
        print key, "\t", str(year[KEY_DATE]), "\t" + str(year[KEY_TEMP])


def coldest_report(data):
    print "Year\t Date\tTemp"
    print "--------------------"
    for key in data:
        year = data[key]
        print key, "\t", str(year[KEY_DATE]), "\t" + str(year[KEY_TEMP])


def analyse_data(data_dir):
    titles = ""
    currentDate = ""
    yearlyData = dict()
    hottestDayData = dict()
    coldestDayData = dict()
    weatherFiles = os.listdir(data_dir)
    if not len(weatherFiles):
        print "data directory is empty"
    else:
        for weatherFile in weatherFiles:
            monthFileName = os.path.abspath(os.path.join(data_dir, weatherFile))
            with open(monthFileName, 'r') as monthlyFile:
                csv_f = csv.reader(monthlyFile)
                titles = []
                for index, row in enumerate(csv_f):
                    if index == 0:
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
                            yearData[KEY_MAX_TEMP] = -99
                            yearData[KEY_MIN_TEMP] = 99
                            yearData[KEY_MAX_HUMD] = -99
                            yearData[KEY_MIN_HUMD] = 99
                            yearlyData[selectedYear] = yearData

                            hottestDay = dict()
                            hottestDay[KEY_DATE] = ""
                            hottestDay[KEY_TEMP] = -99
                            hottestDayData[selectedYear] = hottestDay

                            coldestDay = dict()
                            coldestDay[KEY_DATE] = ""
                            coldestDay[KEY_TEMP] = -99
                            coldestDayData[selectedYear] = coldestDay
                        if dayData[KEY_MAX_TEMP]:
                            if yearlyData[selectedYear][KEY_MAX_TEMP] < int(dayData[KEY_MAX_TEMP]):
                                yearlyData[selectedYear][KEY_MAX_TEMP] = int(dayData[KEY_MAX_TEMP])
                                hottestDayData[selectedYear][KEY_TEMP] = int(dayData[KEY_MAX_TEMP])
                                hottestDayData[selectedYear][KEY_DATE] = currentDate
                        if dayData[KEY_MIN_TEMP]:
                            if yearlyData[selectedYear][KEY_MIN_TEMP] > int(dayData[KEY_MIN_TEMP]):
                                yearlyData[selectedYear][KEY_MIN_TEMP] = int(dayData[KEY_MIN_TEMP])
                                coldestDayData[selectedYear][KEY_TEMP] = int(dayData[KEY_MIN_TEMP])
                                coldestDayData[selectedYear][KEY_DATE] = currentDate
                        if dayData[KEY_MAX_HUMD]:
                            if yearlyData[selectedYear][KEY_MAX_HUMD] < int(dayData[KEY_MAX_HUMD]):
                                yearlyData[selectedYear][KEY_MAX_HUMD] = int(dayData[KEY_MAX_HUMD])
                        if dayData[KEY_MIN_HUMD]:
                            if yearlyData[selectedYear][KEY_MIN_HUMD] > int(dayData[KEY_MIN_HUMD]):
                                yearlyData[selectedYear][KEY_MIN_HUMD] = int(dayData[KEY_MIN_HUMD])
    return {KEY_ANNUAL_DATA: yearlyData, KEY_HOTTEST_DAY_DATA: hottestDayData, KEY_COLDEST_DAY_DATA: coldestDayData}


def main():
    print "**********WEATHERMAN**********"

    analysedData = dict()
    dataDirectory = ""
    reportNumber = ANNUAL_REPORT

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

    if reportNumber == ANNUAL_REPORT:
        annual_report(analysedData[KEY_ANNUAL_DATA])
    if reportNumber == HOTTEST_DAY_REPORT:
        hottest_report(analysedData[KEY_HOTTEST_DAY_DATA])
    if reportNumber == COLDEST_DAY_REPORT:
        coldest_report(analysedData[KEY_COLDEST_DAY_DATA])


if __name__ == '__main__':
    main()
