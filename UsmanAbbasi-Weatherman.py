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
    selected_files = fnmatch.filter(directory_files, '*_weather_*.txt')
    return selected_files


def read_files(new_args, selected_files):
    data = []
    for file_name in selected_files:
        with open(new_args.f + file_name) as read:
            reader = csv.DictReader(read)
            for row in reader:
                data.append(row)

    for record in data:

        if record.get('PKST'):
            record['PKT'] = record['PKST']
            del record['PKST']

        if record['PKT']:
            record['PKT'] = datetime.strptime(record['PKT'], '%Y-%m-%d').date()

        if record['Max TemperatureC']:
            record['Max TemperatureC'] = int(record['Max TemperatureC'])

        if record['Mean TemperatureC']:
            record['Mean TemperatureC'] = int(record['Mean TemperatureC'])

        if record['Min TemperatureC']:
            record['Min TemperatureC'] = int(record['Min TemperatureC'])

        if record['Max Humidity']:
            record['Max Humidity'] = int(record['Max Humidity'])

        if record[' Mean Humidity']:
            record[' Mean Humidity'] = int(record[' Mean Humidity'])

    return data


def convert_args_type(arg):
    if '/' in arg:
        return datetime.strptime(arg, '%Y/%m').date()

    else:
        return datetime.strptime(arg, '%Y').date()


def extract_data(arg, operation, files_data):
    extracted_data = []
    if operation == "-e":
        for data in files_data:
            if arg.year == data['PKT'].year:
                extracted_data.append(data)
        return extracted_data

    if operation == '-a' or operation == '-c':
        for data in files_data:
            if arg.year == data['PKT'].year and arg.month == data['PKT'].month:
                extracted_data.append(data)
        return extracted_data


def calc_max(extracted_data, attribute):
    value = []
    for data in extracted_data:
        if data[attribute]:
            value.append(data[attribute])
    return max(value)


def calc_date(max_temp, min_temp, max_humid, extracted_data):
    max_temp_date = None
    max_humid_date = None
    min_temp_date = None
    for data in extracted_data:
        if max_temp == data['Max TemperatureC']:
            max_temp_date = calendar.month_name[data['PKT'].month] + " " + str(data['PKT'].day)

        if max_humid == data['Max Humidity']:
            max_humid_date = calendar.month_name[data['PKT'].month] + " " + str(data['PKT'].day)

        if min_temp == data['Min TemperatureC']:
            min_temp_date = calendar.month_name[data['PKT'].month] + " " + str(data['PKT'].day)

    return max_temp_date, max_humid_date, min_temp_date


def calc_min(extracted_data, attribute):
    value = []
    for data in extracted_data:
        if data[attribute]:
            value.append(data[attribute])
    return min(value)


def calc_avg(extracted_data, attribute):
    value = []
    for data in extracted_data:
        if data[attribute]:
            value.append(data[attribute])
    avg = (int(sum(value) / len(value)))
    return avg

def bar_chart_bonus(extracted_data):
    max_temp = []
    min_temp = []
    index = 1
    color = ColorText()
    for data in extracted_data:
        if data['Max TemperatureC'] and data['Min TemperatureC']:
            max_temp.append(data['Max TemperatureC'])
            min_temp.append(data['Min TemperatureC'])

    for maxTemp, minTemp in zip(max_temp, min_temp):    #or itertools.zip_longest
        print(color.purple, index, color.blue, "+" * minTemp + color.red, "+" * maxTemp, color.purple, minTemp, "C  -",
              color.purple, maxTemp, "C", color.original)
        index += 1

def bar_chart(extracted_data):
    max_temp = []
    min_temp = []
    index = 1
    color = ColorText()
    for data in extracted_data:
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
        extracted_data = extract_data(args.e, "-e", files_data)
        max_temp = calc_max(extracted_data, "Max TemperatureC")
        min_temp = calc_min(extracted_data, "Min TemperatureC")
        max_humid = calc_max(extracted_data, "Max Humidity")
        max_temp_date, max_humid_date, min_temp_date = calc_date(max_temp, min_temp, max_humid, extracted_data)
        print("Highest:", max_temp, "C on", max_temp_date)
        print("Lowest:", min_temp, "C on", min_temp_date)
        print("Humidity:", max_humid, "% on", max_humid_date)

    if args.a:
        extracted_data = extract_data(args.a, "-a", files_data)
        avg_high_temp = calc_max(extracted_data, "Mean TemperatureC")
        avg_low_temp = calc_min(extracted_data, "Mean TemperatureC")
        avg_mean_humid = calc_avg(extracted_data, " Mean Humidity")
        print("Highest Average:", avg_high_temp, "C")
        print("Lowest Average:", avg_low_temp, "C")
        print("Average Mean Humidity:", avg_mean_humid, "%")

    if args.c:
        extracted_data = extract_data(args.c, "-c", files_data)
        print(calendar.month_name[args.c.month], args.c.year)
        bar_chart(extracted_data)
        bar_chart_bonus(extracted_data)
