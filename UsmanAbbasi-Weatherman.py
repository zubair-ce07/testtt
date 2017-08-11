import fnmatch
import argparse
import os
import calendar
import csv
from datetime import datetime
#import itertools


class ColorText:
    red = '\033[31m'
    purple = '\033[35m'
    blue = '\033[36m'
    original = '\033[0m'


def select_files(new_args):
    directory_files = os.listdir(new_args.f)
    return fnmatch.filter(directory_files, '*_weather_*.txt')


def read_files(new_args, selected_files):
    weather_readings = []
    for file_name in selected_files:
        with open(os.path.join(args.f, file_name)) as file_handle:
            reader = csv.DictReader(file_handle)
            for row in reader:
                weather_readings.append(row)

    for reading in weather_readings:
        if reading.get('PKST'):
            reading['PKT'] = reading['PKST']
            del reading['PKST']

        if reading['PKT']:
            reading['PKT'] = datetime.strptime(reading['PKT'], '%Y-%m-%d').date()
        else:
            reading['PKT'] = '-'

        if reading['Max TemperatureC']:
            reading['Max TemperatureC'] = int(reading['Max TemperatureC'])
        else:
            reading['Max TemperatureC'] = None

        if reading['Mean TemperatureC']:
            reading['Mean TemperatureC'] = int(reading['Mean TemperatureC'])
        else:
            reading['Mean TemperatureC'] = None

        if reading['Min TemperatureC']:
            reading['Min TemperatureC'] = int(reading['Min TemperatureC'])
        else:
            reading['Min TemperatureC'] = None

        if reading['Max Humidity']:
            reading['Max Humidity'] = int(reading['Max Humidity'])
        else:
            reading['Max Humidity'] = None

        if reading[' Mean Humidity']:
            reading[' Mean Humidity'] = int(reading[' Mean Humidity'])
        else:
            reading[' Mean Humidity'] = None
    return weather_readings


def convert_args_type(arg):
    if '/' in arg:
        return datetime.strptime(arg, '%Y/%m').date()

    else:
        return datetime.strptime(arg, '%Y').date()


def filter_readings(arg, operation, files_data):
    selected_readings = []
    if operation == "-e":
        for readings in files_data:
            if arg.year == readings['PKT'].year:
                selected_readings.append(readings)
        return selected_readings

    if operation == '-a' or operation == '-c':
        for readings in files_data:
            if arg.year == readings['PKT'].year and arg.month == readings['PKT'].month:
                selected_readings.append(readings)
        return selected_readings


def calc_max(selected_readings, attribute):
    value = [data[attribute] for data in selected_readings if data[attribute]]
    return max(value)


def calc_date(max_temp, min_temp, max_humid, selected_readings):
    max_temp_date = None
    max_humid_date = None
    min_temp_date = None
    for data in selected_readings:
        date_pattern = calendar.month_name[data['PKT'].month] + " " + str(data['PKT'].day)
        if max_temp == data['Max TemperatureC']:
            max_temp_date = date_pattern

        if max_humid == data['Max Humidity']:
            max_humid_date = date_pattern

        if min_temp == data['Min TemperatureC']:
            min_temp_date = date_pattern

    return max_temp_date, max_humid_date, min_temp_date


def calc_min(selected_readings, attribute):
    value = [data[attribute] for data in selected_readings if data[attribute]]
    return min(value)


def calc_avg(selected_readings, attribute):
    value = [data[attribute] for data in selected_readings if data[attribute]]
    avg = (int(sum(value) / len(value)))
    return avg

def bar_chart_bonus(selected_readings):
    max_temp = []
    min_temp = []
    index = 1
    color = ColorText()
    for data in selected_readings:
        if data['Max TemperatureC'] and data['Min TemperatureC']:
            max_temp.append(data['Max TemperatureC'])
            min_temp.append(data['Min TemperatureC'])

    for maxTemp, minTemp in zip(max_temp, min_temp):    #or itertools.zip_longest
        print(color.purple, index, color.blue, "+" * minTemp + color.red, "+" * maxTemp, color.purple, minTemp, "C  -",
              color.purple, maxTemp, "C", color.original)
        index += 1

def bar_chart(selected_readings):
    max_temp = []
    min_temp = []
    index = 1
    color = ColorText()
    for data in selected_readings:
        if data['Max TemperatureC'] and data['Min TemperatureC']:
            max_temp.append(data['Max TemperatureC'])
            min_temp.append(data['Min TemperatureC'])

    for maxTemp, minTemp in zip(max_temp, min_temp):
        print(color.purple, index, color.red, "+" * maxTemp, color.purple, maxTemp, "C")
        print(color.purple, index, color.blue, "+" * minTemp, color.purple, minTemp, "C", color.original)
        index += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='File directory')
    parser.add_argument('-c', type=convert_args_type, help='-c')
    parser.add_argument('-a', type=convert_args_type, help='-a')
    parser.add_argument('-e', type=convert_args_type, help='-e')
    args = parser.parse_args()
    selected_files = select_files(args)
    files_data = read_files(args, selected_files)
    if args.e:
        selected_readings = filter_readings(args.e, "-e", files_data)
        max_temp = calc_max(selected_readings, "Max TemperatureC")
        min_temp = calc_min(selected_readings, "Min TemperatureC")
        max_humid = calc_max(selected_readings, "Max Humidity")
        max_temp_date, max_humid_date, min_temp_date = calc_date(max_temp, min_temp, max_humid, selected_readings)
        print("Highest:", max_temp, "C on", max_temp_date)
        print("Lowest:", min_temp, "C on", min_temp_date)
        print("Humidity:", max_humid, "% on", max_humid_date)

    if args.a:
        selected_readings = filter_readings(args.a, "-a", files_data)
        avg_high_temp = calc_max(selected_readings, "Mean TemperatureC")
        avg_low_temp = calc_min(selected_readings, "Mean TemperatureC")
        avg_mean_humid = calc_avg(selected_readings, " Mean Humidity")
        print("Highest Average:", avg_high_temp, "C")
        print("Lowest Average:", avg_low_temp, "C")
        print("Average Mean Humidity:", avg_mean_humid, "%")

    if args.c:
        selected_readings = filter_readings(args.c, "-c", files_data)
        print(calendar.month_name[args.c.month], args.c.year)
        bar_chart(selected_readings)
        bar_chart_bonus(selected_readings)
        
