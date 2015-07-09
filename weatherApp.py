# -*- coding: utf-8 -*-
import csv
import os
import sys
import argparse
from enum import Enum

# enum class for catering the option selected by user
class UserChoice(Enum):
    yearly_report = 1
    maxtemp_report = 2
    mintemp_report = 3


# class that will contain the data entries for organized functioning
class WeatherRecord(object):
    def __init__(self, date, maxtemp, mintemp, maxhumid, minhumid):
        self.date = date
        self.maxTemp = maxtemp
        self.minTemp = mintemp
        self.maxHumid = maxhumid
        self.minHumid = minhumid


# contains the logic if user selects option one
# that is generation of Annual report
def yearly_weather_report(yearly_data, yearlist):
    heads = ["Year", "MaxTemp", "MinTemp", " MaxHumid", "MinHumid"]
    print('\t\t'.join(heads))
    print("---------------------------------------------------------------------")
    # going through every year
    for year in yearlist:
        # getting list against year from dictionary
        list_cur = yearly_data[year]
        list_display = []
        list_display.append(year)

        # Sorting list on Max Temp
        list_cur.sort(key=lambda x: x.maxTemp, reverse=True)
        list_display.append(str(list_cur[0].maxTemp))

        # Sorting list on Min Temp
        list_cur.sort(key=lambda x: x.minTemp, reverse=False)
        list_display.append(str(list_cur[0].minTemp))

        # Sorting list on Max humidity
        list_cur.sort(key=lambda x: x.maxHumid, reverse=True)
        list_display.append(str(list_cur[0].maxHumid))

        # Sorting list on Min humidity
        list_cur.sort(key=lambda x: x.minHumid, reverse=False)
        list_display.append(str(list_cur[0].minHumid))

        print('\t\t'.join(list_display))


# contains the logic if user selects option two
# that is generation of Yearly Max temp report
def max_temp_report(yearly_data, yearlist):
    heads = ["Year", "Date", "MaxTemp"]
    print('\t\t'.join(heads))
    print("-----------------------------------------------")
    # going through every year
    for year in yearlist:
        # getting list against year from dictionary
        list_cur = yearly_data[year]

        # Sorting list on Max Temp
        list_cur.sort(key=lambda x: x.maxTemp, reverse=True)

        list_display = []
        list_display.append(year)
        list_display.append(str(list_cur[0].date))
        list_display.append(str(list_cur[0].maxTemp))
        print('\t\t'.join(list_display))


# contains the logic if user selects option two
# that is generation of Yearly Min temp report
def min_temp_report(yearly_data, yearlist):
    heads = ["Year", "Date", "Min Temp"]
    print('\t\t'.join(heads))
    print("--------------------------------------------")

    # going through every year
    for year in yearlist:
        # getting list against year from dictionary
        list_cur = yearly_data[year]
        # Sorting list on Max Temp
        list_cur.sort(key=lambda x: x.minTemp, reverse=False)
        list_display = []
        list_display.append(year)
        list_display.append(str(list_cur[0].date))
        list_display.append(str(list_cur[0].minTemp))
        print('\t\t'.join(list_display))


# instructions for running the code file
def instructions():
    print " "
    print ("Usage: weatherApp​ ​<report#>​ ​<data_dir>")
    print " "
    print ("[Report #]")
    print ("1 for Annual Max/Min Temperature")
    print "2 for Hottest day of each year"
    print "3 for coldest day of each year​"
    print " "
    print "[data_dir]"
    print "Path of Directory containing weather data files"
    print " "


def main():
    # dictionary data struct for having list of data against year
    # i-e [key:value]-> [year: listofusrecords]
    yearly_data = {}

    # simple list of years to avoid hard coding of years
    yearlist = []

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("report")
        parser.add_argument("data_dir_path")
        args = parser.parse_args()
        option = int(args.report)
    except:
        print instructions()
        sys.exit()
    path = args.data_dir_path
    # path = '/home/mateenahmeed/Downloads/weatherdata'

    # checking of Directory path exists or not
    if not os.path.exists(path):
        print("Directory path not found : " + path)
        instructions()
        sys.exit()

    # iterating through every file
    for filename in os.listdir(path):
        # splitting the filename to get the year
        if filename.find("_") is -1:
            print("File in given directory doesnt seems right ")
            sys.exit()
        tokens = filename.split("_")
        year = tokens[2]

        # test list of records for local calculation
        temp_list = []

        # if entry exists against that year in dictionary
        # retrieve the list
        if year in yearly_data:
            temp_list = yearly_data[year]
        # otherwise add new list to dictionary
        else:
            yearly_data[year] = temp_list
            yearlist.append(year)

        # initializing to dummy values
        date = "no date specified"
        minT = 1000
        maxT = (-1000)
        minH = 1000
        maxH = (-1000)

        # opening file
        filepath = path + "/" + filename
        with open(filepath, 'r') as file_current:
            # using csv to read records
            lines = file_current.readlines()[1:-1]
            records = csv.DictReader(lines)
            for row in records:
                date = row.get('PKT') or row.get('PKST')
                if row['Max TemperatureC']:
                    maxT = int(row.get('Max TemperatureC'))
                if row['Min TemperatureC']:
                    minT = int(row.get('Min TemperatureC'))
                if row['Max Humidity']:
                    maxH = int(row.get('Max Humidity'))
                if row[' Min Humidity']:
                    minH = int(row.get(' Min Humidity'))

                # Adding each record to list
                temp_list.append(WeatherRecord(date, maxT, minT, maxH, minH))

        # updating the dictionary with new updated list of records
        yearly_data[year] = temp_list

    # sorting year records to get organized results
    yearlist.sort()

    # function calls against user choice
    if option == UserChoice.yearly_report.value:
        yearly_weather_report(yearly_data, yearlist)  # annual weather report

    elif option == UserChoice.maxtemp_report.value:
        max_temp_report(yearly_data, yearlist)  # max temp report

    elif option == UserChoice.mintemp_report.value:
        min_temp_report(yearly_data, yearlist)  # min temp report

    else:
        instructions()
        sys.exit()


if __name__ == "__main__":
    main()
