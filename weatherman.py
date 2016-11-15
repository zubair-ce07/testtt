import argparse
import glob
import calendar
import csv
from datetime import datetime
from colorama import Fore
import pdb

# read csv and resturn array of hash
def get_weather_data_from_files(folder_path, year, month = "*"):
    # month number to abbreviation
    if month != "*":
        month = calendar.month_abbr[int(month)]

    # get files and make hashes
    files = glob.glob(folder_path + "*_" + year + "_" + month + ".txt")
    data = []
    for file_path in files:
        with open(file_path, "r" ) as file:
            reader = csv.DictReader(file)
            for line in reader:
                data.append(line)

    return data

def to_float(value):
    return float(value or 0)

def format_date(date, input_format = "%Y-%m-%d", output_format = "%B %d"):
    return datetime.strptime(date, input_format).date().strftime(output_format)

def print_weather_stats(nature, value, sign = "", date = ""):

    if (date == ""):
        print(nature + ": " + str(value) + sign)
    else:
        print(nature + ": " + str(value) + sign + " on " + format_date(date))


def temp_and_humid_stats(year, folder_path):
    data = get_weather_data_from_files(folder_path, year)

    highest_temp = data[0]
    lowest_temp = data[0]
    highest_humidity = data[0]

    for row in data:

        if to_float(highest_temp['Max TemperatureC']) < to_float(row['Max TemperatureC']):
            highest_temp = row

        if to_float(lowest_temp['Min TemperatureC']) < to_float(row['Min TemperatureC']):
            lowest_temp = row

        if to_float(highest_humidity['Max Humidity']) < to_float(row['Max Humidity']):
            highest_humidity = row

    # display results
    print_weather_stats("Highest", highest_temp['Max TemperatureC'], "C", highest_temp['PKT'])
    print_weather_stats("Lowest", lowest_temp['Min TemperatureC'], "C", lowest_temp['PKT'])
    print_weather_stats("Humidity", highest_humidity['Max Humidity'], "%", highest_humidity['PKT'])

def average_temp_and_humid_stats(year, month, folder_path):
    data = get_weather_data_from_files(folder_path, year, month)

    highest_temps = []
    lowest_temps = []
    humiditys = []

    for row in data:

        highest_temps.append(to_float(row['Max TemperatureC']))
        lowest_temps.append(to_float(row['Min TemperatureC']))
        humiditys.append(to_float(row['Max Humidity']))

    avg_highest_temp = int(sum(highest_temps) / len(data))
    avg_lowest_temp = int(sum(lowest_temps) / len(data))
    avg_humidity = int(sum(humiditys) / len(data))

    # display results
    print_weather_stats("Highest Average", avg_highest_temp, "C")
    print_weather_stats("Lowest Average", avg_lowest_temp, "C")
    print_weather_stats("Average Mean Humidity", avg_humidity, "%")

def display_horizontal_chart(date, value, color):
    bar = ["+"] * int(value)
    print(format_date(date, "%Y-%m-%d", "%d") + " " + color + "".join(bar) + Fore.RESET + " " + str(int(value)) + "C")

def display_single_horizontal_chart(date, red, blue):
    blue_bar = ["+"] * int(blue)
    red_bar = ["+"] * int(red)
    print(format_date(date, "%Y-%m-%d", "%d") + " " + Fore.BLUE + "".join(blue_bar) + Fore.RED + "".join(red_bar) +
          Fore.RESET + " " + str(int(blue)) + "C - " + str(int(red)) + "C")


def draw_temp_charts(year, month, folder_path):
    data = get_weather_data_from_files(folder_path, year, month)
    print(calendar.month_name[int(month)] + " " + str(year))

    for row in data:
        display_horizontal_chart(row['PKT'], to_float(row['Max TemperatureC']), Fore.RED)
        display_horizontal_chart(row['PKT'], to_float(row['Min TemperatureC']), Fore.BLUE)

def draw_temp_charts_single_line(year, month, folder_path):
    data = get_weather_data_from_files(folder_path, year, month)
    print(calendar.month_name[int(month)] + " " + str(year))

    for row in data:
        display_single_horizontal_chart(row['PKT'], to_float(row['Max TemperatureC']),
                                        to_float(row['Min TemperatureC']))

def main():
    # for parsing command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path')
    parser.add_argument('-e')
    parser.add_argument('-a')
    parser.add_argument('-c')

    args = parser.parse_args()
    if args.e:
        temp_and_humid_stats(args.e, args.folder_path)
        print(" ")

    if args.a:
        year, month = args.a.split('/')
        average_temp_and_humid_stats(year, month, args.folder_path)
        print(" ")

    if args.c:
        year, month = args.c.split('/')
        draw_temp_charts(year, month, args.folder_path)
        print(" ")

        draw_temp_charts_single_line(year, month, args.folder_path)
        print(" ")

if __name__ == "__main__":
    main()