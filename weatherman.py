#!/usr/bin/python3.5

import os
import argparse
import csv
from enum import Enum


class Months(Enum):
    # Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec = range(1,12)[0:11]
    Jan = 1
    Feb = 2
    Mar = 3
    Apr = 4
    May = 5
    Jun = 6
    Jul = 7
    Aug = 8
    Sep = 9
    Oct = 10
    Nov = 11
    Dec = 12


def open_file(path, filename):
    list_buffer_dict=[]
    with open(path + filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            list_buffer_dict.append(row)

    return list_buffer_dict


def get_yearmonth_split(option):
    option_list = option.split("/")
    year = int(option_list[0])
    month = int(option_list[1])

    return year, month


def yearly_report(path, year):
    wildcard_start = "Murree_weather_"+str(year)+'_'
    data_present = 0
    year_buffer = []
    for file in os.listdir(path):
        if file.startswith(wildcard_start):
            data_present = 1
            file_buffer = open_file(path, file)
            year_buffer.append(file_buffer)

    if data_present == 0:
        print("Data Not Available")
        return

    max_temp = [-1, -1, -1]
    min_temp = [-1, -1, 9999]
    max_humidity = [-1, -1, -1]
    for i in range(0, len(year_buffer)):
        if year_buffer[i]:
            for j in range(0, len(year_buffer[i])):
                temp_max = (year_buffer[i][j]['Max TemperatureC'])
                temp_min = (year_buffer[i][j]['Min TemperatureC'])
                humidity_max = (year_buffer[i][j]['Max Humidity'])
                today = str.split(year_buffer[i][j]['PKT'], '-')

                if temp_max:
                    if int(temp_max) > max_temp[2]:
                        max_temp = [int(today[1]), int(today[2]), int(temp_max)]
                if temp_min:
                    if int(temp_min) < min_temp[2]:
                        min_temp = [int(today[1]), int(today[2]), int(temp_min)]
                if humidity_max:
                    if int(humidity_max) > max_humidity[2]:
                        max_humidity = [int(today[1]), int(today[2]), int(humidity_max)]

    print("Highest: %sC on %s %s" % (max_temp[2], Months(max_temp[0]).name, max_temp[1]))
    print("Lowest: %sC on %s %s" % (min_temp[2], Months(min_temp[0]).name, min_temp[1]))
    print("Humidity: %s%% on %s %s" % (max_humidity[2], Months(max_humidity[0]).name, max_humidity[1]))

    print()
    return


def monthly_report(path, year, month):
    if month > 12 or month < 1:
        print("Invalid Month Entry")
        return

    max_temp_list = []
    min_temp_list = []
    mean_humidity_list = []

    filename = "Murree_weather_"+str(year)+'_'+str(Months(month).name)+".txt"
    if os.path.isfile(path+filename):
        month_buffer = open_file(path, filename)
        for j in range(0, len(month_buffer)):
            temp_max = (month_buffer[j]['Max TemperatureC'])
            temp_min = (month_buffer[j]['Min TemperatureC'])
            humidity_mean = (month_buffer[j][' Mean Humidity'])

            if temp_max:
                max_temp_list.append(int(temp_max))
            if temp_min:
                min_temp_list.append(int(temp_min))
            if humidity_mean:
                mean_humidity_list.append(int(humidity_mean))

        avg_max_temp = sum(max_temp_list)//len(max_temp_list)
        avg_min_temp = sum(min_temp_list)//len(min_temp_list)
        avg_mean_humidity = sum(mean_humidity_list)//len(mean_humidity_list)

        print("Highest Average: ", avg_max_temp)
        print("Lowest Average: ", avg_min_temp)
        print("Average Mean Humidity: %d%%" % avg_mean_humidity)
    else:
        print("Data Not Available")

    print()
    return


def daily_report(path, year, month):
    if month > 12 or month < 1:
        print("Invalid Month Entry")
        return

    filename = "Murree_weather_" + str(year) + '_' + str(Months(month).name) + ".txt"
    if os.path.isfile(path + filename):
        month_buffer = open_file(path, filename)
        print(str(Months(month).name), year)
        for j in range(0, len(month_buffer)):
            temp_max = (month_buffer[j]['Max TemperatureC'])
            temp_min = (month_buffer[j]['Min TemperatureC'])
            today = str.split(month_buffer[j]['PKT'], '-')
            if temp_max:
                barmax = "+"*int(temp_max)
            if temp_min:
                barmin = '+'*int(temp_min)
            if temp_min and temp_max:
                barmax = "+"*int(temp_max)
                barmin = '+'*int(temp_min)
                print("%s \033[1;31;48m%s\033[0m\033[1;34;48m%s\033[0m %sC-%sC" % (today[2], barmin, barmax, temp_min, temp_max))
    else:
        print("Data Not Available")

    print()
    return


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('path',  type=str)
    parser.add_argument('-e', dest="year_param", type=int)
    parser.add_argument('-a', dest="month_param", type=str)
    parser.add_argument('-c', dest="day_param", type=str)
    args = parser.parse_args()
    path = args.path + '/'

    if args.year_param:
        yearly_in1 = args.year_param
        yearly_report(path, yearly_in1)
    if args.month_param:
        monthly_in1, monthly_in2 = get_yearmonth_split(args.month_param)
        monthly_report(path, monthly_in1, monthly_in2)
    if args.day_param:
        daily_in1, daily_in2 = get_yearmonth_split(args.day_param)
        daily_report(path, daily_in1, daily_in2)

    return


if __name__ == "__main__":
    os.system('clear')
    main()

