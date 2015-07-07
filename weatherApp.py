# -*- coding: utf-8 -*-
import os
import sys


# class that will contain the data entries for organized functioning
class DetailInfo:

    def __init__(self, date, maxtemp, mintemp, maxhumid, minhumid):
        self.date = date
        self.maxTemp = maxtemp
        self.minTemp = mintemp
        self.maxHumid = maxhumid
        self.minHumid = minhumid


# contains the logic if user selects option one
# that is generation of Annual report
def option1():
    print("Year     MaxTemp     MinTemp     MaxHumid    MinHumid")
    print("-----------------------------------------------------")
    # going through every year
    for year in yearlist:

        # getting list against year from dictionary
        list_cur = my_dict[year]

        # Sorting list on Max Temp
        list_cur.sort(key = lambda x: x.maxTemp, reverse = True)
        # this loop will find the true value
        # because there are some dummy values
        # this wont be inefficient
        #  because value will be found in less than 10 tries
        pos = 0
        while True:
            if (list_cur[pos].maxTemp == "Max TemperatureC") or \
                    (list_cur[pos].maxTemp == ""):
                pos = pos + 1
            else:
                maxT = list_cur[pos].maxTemp
                break

        # Sorting list on Min Temp
        list_cur.sort(key = lambda x: x.minTemp, reverse = False)
        pos = 0
        # same upper Loop
        while True:
            if (list_cur[pos].minTemp == "Min TemperatureC") or \
                    (list_cur[pos].minTemp == ""):
                pos = pos + 1
            else:
                minT = list_cur[pos].minTemp
                break


        # Sorting list on Min humidity
        list_cur.sort(key = lambda x: x.minHumid, reverse = False)
        pos = 0
        # same loop
        while True:
            if (list_cur[pos].minHumid == " Min Humidity") or \
                    (list_cur[pos].minHumid == ""):
                pos = pos + 1
            else:
                minH = list_cur[pos].minHumid
                break

        # Sorting list on Max humidity
        list_cur.sort(key = lambda x: x.maxHumid, reverse = True)
        pos = 0
        # same loop
        while True:
            if (list_cur[pos].maxHumid == "Max Humidity") or \
                    (list_cur[pos].maxHumid == ""):
                pos = pos + 1
            else:
                maxH = list_cur[pos].maxHumid
                break

        print(year + "       " + maxT + "          " + minT +
              "          " + maxH + "           " + minH)


# contains the logic if user selects option two
# that is generation of Yearly Max temp report
def option2():
    print("Year          Date        Max temp")
    print("-------------------------------")
    # going through every year
    for year in yearlist:
        # getting list against year from dictionary
        list_cur = my_dict[year]

        # Sorting list on Max Temp
        list_cur.sort(key = lambda x: x.maxTemp, reverse = True)

        # this loop will find the true value
        pos = 0
        while True:
            if (list_cur[pos].maxTemp == "Max TemperatureC") or \
                    (list_cur[pos].maxTemp == ""):
                pos = pos + 1
            else:
                print(year + "       " + list_cur[pos].date +
                      "          " + list_cur[pos].maxTemp)
                break


# contains the logic if user selects option two
# that is generation of Yearly Min temp report
def option3():
    print("Year          Date        Min Temp")
    print("-----------------------------------")

    # going through every year
    for year in yearlist:
        # getting list against year from dictionary
        list_cur = my_dict[year]
        # Sorting list on Max Temp
        list_cur.sort(key = lambda x: x.minTemp, reverse = False)

        # this loop will find the true value
        pos = 0
        while True:
            if (list_cur[pos].minTemp == "Min TemperatureC") or \
                    (list_cur[pos].minTemp == ""):
                pos = pos + 1
            else:
                minT = list_cur[pos].minTemp
                print(year + "       " + list_cur[pos].date +
                      "          " + list_cur[pos].minTemp)
                break


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

# dictionary data struct for having list of data against year
# i-e [key:value]-> [year: listofusrecords]
my_dict = {}
# simple list of years to avoid hard coding of years
yearlist = []

# argument list check
if len(sys.argv) != 3:
    instructions()
    sys.exit()
try:
    option = int(sys.argv[1])
except:
    instructions()
    sys.exit()
path = sys.argv[2]
# path = '/home/mateenahmeed/Downloads/weatherdata'

# checking of Directory path exists or not
if not os.path.exists(path):
    print("Directory path not found : " + path)
    instructions()
    sys.exit()

# iterating through every file
for filename in os.listdir(path):
    # splitting the filename to get the year
    tokens = filename.split("_")
    year = tokens[2]

    # test list of records for local calculation
    list1 = []

    # if entry exists against that year in dictionary
    # retrieve the list
    if year in my_dict:
        list1 = my_dict[year]
    # otherwise add new list to dictionary
    else:
        my_dict[year] = list1
        yearlist.append(year)

    # opening file
    file = open(path + "/" + filename, 'r')
    # going through line by line
    for line in file:
        # splitting data on teh basis of comma
        details = line.split(",")

        # length check is to avoid last lines that are extra in each file
        if len(details) > 1:

            date = details[0]
            maxT = details[1]
            # zero is padded to single digits to get correct
            # sorting results as everything is in string format
            if len(maxT) == 1:
                maxT = "0" + maxT
            minT = details[3]
            if len(minT) == 1:
                minT = "0" + minT
            maxH = details[7]
            if len(maxH) == 1:
                maxH = "0" + maxT
            minH = details[9]
            if len(minH) == 1:
                minH = "0" + minH
            # Adding each record to list
            list1.append(DetailInfo(date, maxT, minT, maxH, minH))

    file.close()

    # updating the dictionary with new updated list of records
    my_dict[year] = list1

# sorting year records to get organized results
yearlist.sort()

# function calls against user choice
if option == 1:
    option1()       # annual report
if option == 2:
    option2()       # max temp report
if option == 3:
    option3()       # min temp report
