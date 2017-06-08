#!/usr/bin/env python3
from time import monotonic

__author__ = 'ruhaib'

import os
import pandas
import calendar
import datetime
#import sys
import argparse
from termcolor import colored
import math



def year_range(string):



    if (string.find('/') == -1):

        year_passed = int(string)

        if( year_passed > 2011 or year_passed < 1996):
            msg = '%r year passed is out of range' % string
            raise argparse.ArgumentTypeError(msg)

        return year_passed

    else:

        msg = '%r only year is required the input is incorrect' % string
        raise argparse.ArgumentTypeError(msg)

def year_month_validity(string):

    if(string.count('/') != 1):
        msg = '%r incorrect month and year passed' % string
        raise argparse.ArgumentTypeError(msg)

    year_passed = int(string.split("/")[0])
    month_passed = int(string.split("/")[1])

    if( year_passed > 2011 or year_passed < 1996):
        msg = "%r year passed is out of range" % string
        raise argparse.ArgumentTypeError(msg)

    if( month_passed > 12 or month_passed < 1):
        msg = "%r month, passed is out of range" % string
        raise argparse.ArgumentTypeError(msg)

    return string



def show_task1_requirements(weather_data, year, pathToFiles):

    y = int(year)

    files_names_of_year = weather_data[weather_data[0].str.contains("lahore_weather_"+str(year))]


    maxTemp = -100000
    maxDate = 0
    maxMonth = 'Jan'
    minTemp = 100000
    minDate = 0
    minMonth = 'jan'
    humid = -100000
    humidDate = 100000
    humidMonth = 'jan'


    for index,row in files_names_of_year.iterrows():

        data_of_month = pandas.read_csv(pathToFiles+"/"+row[0], header=0)

        if(data_of_month['Max TemperatureC'].max() > maxTemp):
            tempMaxTemperature = data_of_month.loc[data_of_month['Max TemperatureC'] == data_of_month['Max TemperatureC'].max()]
            maxTemp = data_of_month['Max TemperatureC'].max()
            date = datetime.datetime.strptime(tempMaxTemperature[tempMaxTemperature.columns[0]].iloc[0], "%Y-%m-%d")
            maxDate = date.day
            maxMonth = calendar.month_name[date.month]

        if(data_of_month['Min TemperatureC'].min() < minTemp):
            minTemp = data_of_month['Min TemperatureC'].min()
            tempMaxTemperature = data_of_month.loc[data_of_month['Min TemperatureC'] == data_of_month['Min TemperatureC'].min()]
            date = datetime.datetime.strptime(tempMaxTemperature[tempMaxTemperature.columns[0]].iloc[0], "%Y-%m-%d")
            minDate = date.day
            minMonth = calendar.month_name[date.month]

        if(data_of_month['Max Humidity'].max() > humid):
            humid = data_of_month['Max Humidity'].max()
            tempMaxTemperature = data_of_month.loc[data_of_month['Max Humidity'] == data_of_month['Max Humidity'].max()]
            date = datetime.datetime.strptime(tempMaxTemperature[tempMaxTemperature.columns[0]].iloc[0], "%Y-%m-%d")
            humidDate = date.day
            humidMonth = calendar.month_name[date.month]


    print("Highest: %dC on %s %d" % (maxTemp, maxMonth, maxDate))
    print("Lowest: %dC on %s %d" % (minTemp, minMonth, minDate))
    print("Humid: %d%% on %s %d" % (humid, humidMonth, humidDate))


def show_task2_requirements(weather_data, date, pathToFiles):

    y = int(date.split("/")[0])


    #extracting path of the file required
    tempDF = weather_data[weather_data[0].str.contains("lahore_weather_"+str(y))]
    abbr = calendar.month_abbr[int(date.split("/")[1])]
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


def show_task3_graphs(weather_data, date, pathToFiles):

    y = int(date.split("/")[0])


    #extracting path of the file required
    tempDF = weather_data[weather_data[0].str.contains("lahore_weather_"+str(y))]
    abbr = calendar.month_name[int(date.split("/")[1])]
    print("%s %d" % (abbr,y))
    abbr = calendar.month_abbr[int(date.split("/")[1])]
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




def main():

    parser = argparse.ArgumentParser(description='WeatherMan data extraction.')

    parser.add_argument(
        '-e',type=year_range,
        help='(usage: -e yyyy) to see maximum temperature, minimum temperature and humidity')

    parser.add_argument(
        '-a',type=year_month_validity,
        help='(usage: -a yyyy/mm) to see average maximum, average minimum temperature and mean humidity of the month')

    parser.add_argument(
        '-c', type=year_month_validity,
        help='(usage: -c yyyy/mm) to see horizontal bar chart of highest and lowest temperature on each day')

    parser.add_argument('path',
                        help='path to the files having weather data')


    args = parser.parse_args()

    if not (os.path.isdir(args.path)):
        print("path to directory does not exist")
        quit()


    weather_data = pandas.DataFrame(os.listdir(args.path))


    if args.e:

        show_task1_requirements(weather_data, args.e, args.path)

    if args.a:

        show_task2_requirements(weather_data, args.a, args.path)

    if args.c:

        show_task3_graphs(weather_data, args.c, args.path)


if __name__ == "__main__":
    main()