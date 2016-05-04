# -*- coding: utf-8 -*-
import os

KEY_YEAR = "year"
KEY_DATE = "date"
KEY_TEMP = "temp"

KEY_MAX_TEMP = "Max TemperatureC";
KEY_MIN_TEMP = "Min TemperatureC";
KEY_MAX_HUMD = "Max Humidity"
KEY_MIN_HUMD = "Min Humidity"


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


def main():
    print "**********WEATHERMAN**********"

    titles = ""
    currentDate = ""
    yearlyData = dict()
    hottestDayData = dict()
    coldestDayData = dict()

    reportNumber = raw_input("Please enter \n1 for Annual Max/Min Temperature\n2 for Hottest day of each year\n"
                             "3 for coldest day of each year​\n")
    data_dir = raw_input("Please enter data directory path for weather files\n")

    if reportNumber == "" or data_dir == "":
        print "Please provide Report number and Data Directory Path"

    try:
        weatherFiles = os.listdir(data_dir)
        if len(weatherFiles) == 0:
            print "data directory is empty"
        else:
            for weatherFile in weatherFiles:
                monthFileName = os.path.abspath(os.path.join(data_dir, weatherFile))
                with open(monthFileName, 'r') as monthlyFile:
                    if monthlyFile.readline() == "\r\n":
                        titles = monthlyFile.readline().strip().split(",")
                    for day in monthlyFile:
                        dayData = dict()
                        if not day.__contains__("<!--"):
                            parsedDayList = day.strip().split(",")
                            for index, title in enumerate(titles):
                                dayData[str.strip(title)] = parsedDayList[index]
                            if 'PKT' in dayData:
                                currentDate = str(dayData['PKT'])
                                selectedYear = int(str(dayData['PKT']).split("-").__getitem__(0))
                            elif 'PKST' in dayData:
                                currentDate = str(dayData['PKST'])
                                selectedYear = int(str(dayData['PKST']).split("-").__getitem__(0))
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
                            if dayData[KEY_MAX_TEMP] != '':
                                if yearlyData[selectedYear][KEY_MAX_TEMP] < int(dayData[KEY_MAX_TEMP]):
                                    yearlyData[selectedYear][KEY_MAX_TEMP] = int(dayData[KEY_MAX_TEMP])
                                    hottestDayData[selectedYear][KEY_TEMP] = int(dayData[KEY_MAX_TEMP])
                                    hottestDayData[selectedYear][KEY_DATE] = currentDate
                            if dayData[KEY_MIN_TEMP] != '':
                                if yearlyData[selectedYear][KEY_MIN_TEMP] > int(dayData[KEY_MIN_TEMP]):
                                    yearlyData[selectedYear][KEY_MIN_TEMP] = int(dayData[KEY_MIN_TEMP])
                                    coldestDayData[selectedYear][KEY_TEMP] = int(dayData[KEY_MIN_TEMP])
                                    coldestDayData[selectedYear][KEY_DATE] = currentDate
                            if dayData[KEY_MAX_HUMD] != '':
                                if yearlyData[selectedYear][KEY_MAX_HUMD] < int(dayData[KEY_MAX_HUMD]):
                                    yearlyData[selectedYear][KEY_MAX_HUMD] = int(dayData[KEY_MAX_HUMD])
                            if dayData[KEY_MIN_HUMD] != '':
                                if yearlyData[selectedYear][KEY_MIN_HUMD] > int(dayData[KEY_MIN_HUMD]):
                                    yearlyData[selectedYear][KEY_MIN_HUMD] = int(dayData[KEY_MIN_HUMD])

            print "You pressed " + reportNumber
            if reportNumber == "1":
                annual_report(yearlyData)
            if reportNumber == "2":
                hottest_report(hottestDayData)
            if reportNumber == "3":
                coldest_report(coldestDayData)
    except OSError:
        print "Not a Directory Path"

if __name__ == '__main__':
    main()
