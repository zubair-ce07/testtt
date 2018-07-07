import calendar as cal
import datetime as dt
import csv
import argparse
import utility as ut


class DayForecast:

    def __init__(self, read_list):
        self.date = read_list[0]
        self.max_temp = read_list[1]
        self.mean_temp = read_list[2]
        self.min_temp = read_list[3]
        self.max_humidity = read_list[7]
        self.mean_humidity = read_list[8]
        self.min_humidity = read_list[9]


# CONSTANTS
WEATHER_CITY = "Murree_weather"
YEAR_LENGTH = 12


# def get_month(string):
#     temp = string.year_month.split("/")
#     return cal.month_name[int(temp[1])], temp[0]
#

def get_month(string):
    return string[:3]


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Directory to all weather files", type=str)
    parser.add_argument("-e", "--e", help="Option E for Min Max", action="append")
    parser.add_argument("-a", "--a", help="Option A for Min Max", action="append")
    parser.add_argument("-c", "--c", help="Option C for Min Max", action="append")
    return parser.parse_args()


def parse_files(directory, read_list):
    year = 2016
    year_list = list(range(year, year - 13, -1))

    for i in range(0, len(year_list)):
        for j in range(0, YEAR_LENGTH):
            file_location = ut.get_file_location(year_list[i], get_month(cal.month_name[j + 1]),
                                                 WEATHER_CITY, directory)
            try:
                weather_file = open(file_location, "r")
                reader = csv.reader(weather_file)
                temp_readings = list(reader)

                for j in range(1, len(temp_readings)):
                    read_list.append(DayForecast(temp_readings[j]))

            except:
                print("File at location %s not found" % file_location)


def calculate_results(readings):
    print("HERE")


def generate_bar_chart(max_temp, min_temp, day):
    print("0%d " % day, end="")
    for i in range(0, max_temp + min_temp):
        if i < min_temp:
            ut.print_blue("+")
        else:
            ut.print_red("+")

    print(" %dC - %dC" % (min_temp, max_temp))


def high_temp_bar_chart(max_temp, day):
    print("0%d " % day, end="")
    for i in range(0, max_temp):
        print(colored('+', 'red'), end="")
    print(" %dC" % max_temp)


def low_temp_bar_chart(min_temp, day):
    print("0%d " % day, end="")
    for i in range(0, min_temp):
        print(colored('+', 'blue'), end="")
    print(" %dC" % min_temp)


def generate_monthly_report(avg_max_temp, avg_lowest_temp, avg_mean_humidity):
    print("Highest Average: %dC" % avg_max_temp)
    print("Lowest Average: %dC" % avg_lowest_temp)
    print("Average Mean Humidity: %d%%" % avg_mean_humidity)


def generate_yearly_report(max_temp, max_temp_month, max_temp_day,
                           min_temp, min_temp_month, min_temp_day,
                           max_humidity, max_humidity_month, max_humidity_day):
    print("Highest: %dC on %s %d" %
          (max_temp,
           max_temp_month,
           max_temp_day))

    print("Lowest: %dC on %s %d" %
          (min_temp,
           min_temp_month,
           min_temp_day))

    print("Humidity: %d%% on %s %d" %
          (max_humidity,
           max_humidity_month,
           max_humidity_day))


def main(args):
    readings_list = []
    parse_files(args, readings_list)
    calculate_results(readings_list)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
