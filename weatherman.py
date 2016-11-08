#!/usr/bin/python3.5

import os
import argparse
import csv
from enum import Enum


class Months(Enum):
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
    buffer = []
    with open(path + filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            buffer.append(row)

    return buffer


def get_yearmonth_split(options):
    options_separate = options.split("/")
    year = int(options_separate[0])
    month = int(options_separate[1])

    return year, month


def yearly_report(path, year):
    wildcard_start = "Murree_weather_{0}_".format(str(year))
    year_buffer = []
    for file in os.listdir(path):
        if file.startswith(wildcard_start):
            file_buffer = open_file(path, file)
            year_buffer.append(file_buffer)

    if not year_buffer:
        print("Data Not Available\n")
        return

    max_temp = {'Month': -1, 'Day': -1, 'Value': -1}
    min_temp = {'Month': -1, 'Day': -1, 'Value': 9999}
    max_humidity = {'Month': -1, 'Day': -1, 'Value': -1}
    for i in range(0, len(year_buffer)):
        if year_buffer[i]:
            for j in range(0, len(year_buffer[i])):
                current_max_temp = (year_buffer[i][j]['Max TemperatureC'])
                current_min_temp = (year_buffer[i][j]['Min TemperatureC'])
                current_max_humidity = (year_buffer[i][j]['Max Humidity'])
                today_separate = str.split(year_buffer[i][j]['PKT'], '-')
                today = {'Year': int(today_separate[0]), 'Month': int(today_separate[1]), 'Day': int(today_separate[2])}

                if current_max_temp:
                    if int(current_max_temp) > max_temp['Value']:
                        max_temp['Month'], max_temp['Day'], max_temp['Value'] = today['Month'],\
                                                                                today['Day'],\
                                                                                int(current_max_temp)
                if current_min_temp:
                    if int(current_min_temp) < min_temp['Value']:
                        min_temp['Month'], min_temp['Day'], min_temp['Value'] = today['Month'],\
                                                                                today['Day'],\
                                                                                int(current_min_temp)
                if current_max_humidity:
                    if int(current_max_humidity) > max_humidity['Value']:
                        max_humidity['Month'], max_humidity['Day'], max_humidity['Value'] = today['Month'], \
                                                                                            today['Day'],\
                                                                                            int(current_max_humidity)

    print("Highest: {0}C on {1} {2}".format(max_temp['Value'], Months(max_temp['Month']).name, max_temp['Day']))
    print("Lowest: {0}C on {1} {2}".format(min_temp['Value'], Months(min_temp['Month']).name, min_temp['Day']))
    print("Humidity: {0}% on {1} {2}\n".format(max_humidity['Value'], Months(max_humidity['Month']).name,
                                               max_humidity['Day']))

    return


def monthly_report(path, year, month):
    if not 1 <= month <= 12:
        print("Invalid Month Entry for Monthly Report\n")
        return

    max_temp = []
    min_temp = []
    mean_humidity = []

    filename = "Murree_weather_{0}_{1}.txt".format(str(year), str(Months(month).name))
    if os.path.isfile(path+filename):
        month_buffer = open_file(path, filename)
        for j in range(0, len(month_buffer)):
            current_max_temp = (month_buffer[j]['Max TemperatureC'])
            current_min_temp = (month_buffer[j]['Min TemperatureC'])
            current_mean_humidity = (month_buffer[j][' Mean Humidity'])

            if current_max_temp:
                max_temp.append(int(current_max_temp))
            if current_min_temp:
                min_temp.append(int(current_min_temp))
            if current_mean_humidity:
                mean_humidity.append(int(current_mean_humidity))

        avg_max_temp = sum(max_temp)//len(max_temp)
        avg_min_temp = sum(min_temp)//len(min_temp)
        avg_mean_humidity = sum(mean_humidity)//len(mean_humidity)

        print("Highest Average: {0}C".format(avg_max_temp))
        print("Lowest Average: {0}C".format(avg_min_temp))
        print("Average Mean Humidity: {0}%\n".format(avg_mean_humidity))
    else:
        print("Data Not Available\n")

    return


def daily_report(path, year, month):
    if not 1 <= month <= 12:
        print("Invalid Month Entry for Daily report\n")
        return

    filename = "Murree_weather_{0}_{1}.txt".format(str(year), str(Months(month).name))
    if os.path.isfile(path + filename):
        month_buffer = open_file(path, filename)
        print(str(Months(month).name), year)
        for j in range(0, len(month_buffer)):
            current_max_temp = (month_buffer[j]['Max TemperatureC'])
            current_min_temp = (month_buffer[j]['Min TemperatureC'])
            today_separate = str.split(month_buffer[j]['PKT'], '-')
            today = {'Year': int(today_separate[0]), 'Month': int(today_separate[1]), 'Day': int(today_separate[2])}
            if current_min_temp and current_max_temp:
                bar_max = "+"*int(current_max_temp)
                bar_min = '+'*int(current_min_temp)
                print("{0} \033[1;31;48m{1}\033[0m\033[1;34;48m{2}\033[0m {3}C-{4}C".format(today['Day'],
                                                                                            bar_min,
                                                                                            bar_max,
                                                                                            current_min_temp,
                                                                                            current_max_temp))
            elif current_max_temp:
                bar_max = "+"*int(current_max_temp)
                print("{0} \033[1;34;48m{1}\033[0m {2}C".format(today['Day'], bar_max, current_max_temp))
            elif current_min_temp:
                bar_min = '+'*int(current_min_temp)
                print("{0} \033[1;31;48m{1}\033[0m {2}C".format(today['Day'], bar_min, current_min_temp))

    else:
        print("Data Not Available\n")

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
