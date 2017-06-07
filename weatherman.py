__author__ = 'ruhaib'

import os
import pandas
import calendar
import datetime
import sys
from termcolor import colored
import math

mode = sys.argv[1]
year = sys.argv[2]
pathToFiles = sys.argv[3]


if(mode == "-e"):

    if not (os.path.isdir(pathToFiles)):
        print("path to directory does not exist")
        quit()

    df = pandas.DataFrame(os.listdir(pathToFiles))

    y = int(year)

    if( y > 2011 or y < 1996):
        print("year passed is incorrect")
        quit()

    tempDF = df[df[0].str.contains("lahore_weather_"+str(year))]


    maxTemp = -100000
    maxDate = 0
    maxMonth = 'Jan'
    minTemp = 100000
    minDate = 0
    minMonth = 'jan'
    humid = -100000
    humidDate = 100000
    humidMonth = 'jan'


    for index,row in tempDF.iterrows():

        data = pandas.read_csv(pathToFiles+"/"+row[0], header=0)

        if(data['Max TemperatureC'].max() > maxTemp):
            tempMaxTemperature = data.loc[data['Max TemperatureC'] == data['Max TemperatureC'].max()]
            maxTemp = data['Max TemperatureC'].max()
            date = datetime.datetime.strptime(tempMaxTemperature[tempMaxTemperature.columns[0]].iloc[0], "%Y-%m-%d")
            maxDate = date.day
            maxMonth = calendar.month_name[date.month]

        if(data['Min TemperatureC'].min() < minTemp):
            minTemp = data['Min TemperatureC'].min()
            tempMaxTemperature = data.loc[data['Min TemperatureC'] == data['Min TemperatureC'].min()]
            date = datetime.datetime.strptime(tempMaxTemperature[tempMaxTemperature.columns[0]].iloc[0], "%Y-%m-%d")
            minDate = date.day
            minMonth = calendar.month_name[date.month]

        if(data['Max Humidity'].max() > humid):
            humid = data['Max Humidity'].max()
            tempMaxTemperature = data.loc[data['Max Humidity'] == data['Max Humidity'].max()]
            date = datetime.datetime.strptime(tempMaxTemperature[tempMaxTemperature.columns[0]].iloc[0], "%Y-%m-%d")
            humidDate = date.day
            humidMonth = calendar.month_name[date.month]


    print("Highest: %dC on %s %d" % (maxTemp, maxMonth, maxDate))
    print("Lowest: %dC on %s %d" % (minTemp, minMonth, minDate))
    print("Humid: %d%% on %s %d" % (humid, humidMonth, humidDate))

elif (mode == "-a"):

    if not (os.path.isdir(pathToFiles)):
        print("path to directory does not exist")
        quit()

    df = pandas.DataFrame(os.listdir(pathToFiles))
    y = int(year.split("/")[0])

    if( y > 2011 | y < 1996):
        print("year passed is incorrect")
        quit()

    #extracting path of the file required
    tempDF = df[df[0].str.contains("lahore_weather_"+str(y))]
    abbr = calendar.month_abbr[int(year.split("/")[1])]
    monthFile = pathToFiles+"/"+tempDF[tempDF[0].str.contains("lahore_weather_"+str(y)+"_"+abbr)][0].iloc[0]


    data = pandas.read_csv(monthFile, header=0)

    #extracting average highest temperature
    maxTemp = data[data.columns[2]].max()

    #extracting average lowest temperature
    minTemp = data[data.columns[2]].min()

    #extracting average humidity
    humid = data[data.columns[8]].sum()/data[data.columns[8]].count()

    print("Highest Average: %dC" % maxTemp)
    print("Lowest Average: %dC" % minTemp)
    print("Average Humidity: %d%%" % humid)

elif (mode == "-c"):

    if not (os.path.isdir(pathToFiles)):
        print("path to directory does not exist")
        quit()

    df = pandas.DataFrame(os.listdir(pathToFiles))
    y = int(year.split("/")[0])

    if( y > 2011 | y < 1996):
        print("year passed is incorrect")
        quit()

    #extracting path of the file required
    tempDF = df[df[0].str.contains("lahore_weather_"+str(y))]
    abbr = calendar.month_name[int(year.split("/")[1])]
    print("%s %d" % (abbr,y))
    abbr = calendar.month_abbr[int(year.split("/")[1])]
    monthFile = pathToFiles+"/"+tempDF[tempDF[0].str.contains("lahore_weather_"+str(y)+"_"+abbr)][0].iloc[0]

    data = pandas.read_csv(monthFile, header=0)

    days = 1
    for index,row in data.iterrows():

        if not (math.isnan(row[3])) and not (math.isnan(row[1])):
            print(days,end = '')
            print(' ',end='')
            text=""

            for i in range(0,int(row[3])):
                text += colored('+',"blue")
                print(text,end='')

            text=""

            for i in range(0,int(row[1])):
                text += colored('+',"red")
                print(text,end='')

            days+=1
            print("%dC - %dC"%(row[3],row[1]))
else:

    print("%s is not a valid parameter" % mode)
