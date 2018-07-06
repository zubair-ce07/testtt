import calendar as cal
import argparse
import utility as ut
import sys


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


def get_argument_list():
    index = 0
    for i in range(0, TOTAL_REPORTS):
        argument_list.append(Argument(temp_list[i + index], temp_list[i + index + 1]))
        index += 1


def get_month(str):
    temp = str.year_month.split("/")
    return cal.month_name[int(temp[1])], temp[0]


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Directory to all weather files", type=str)
    parser.add_argument("-e", "--e", help="Option E for Min Max", action="append")
    parser.add_argument("-a", "--a", help="Option A for Min Max", action="append")
    parser.add_argument("-c", "--c", help="Option C for Min Max", action="append")

    return parser.parse_args()


def parse_files(args, read_list):
    if args.e:
        # for i in range(0, YEAR_LENGTH):
        #     file_location = ut.get_file_location(arg_list_row.year_month, month_tuple[i],
        #                                          WEATHER_CITY, directory)
        #     try:
        #         weather_file = open(file_location, "r")
        #         temp_readings = [line.split(",") for line in weather_file]
        #
        #         for j in range(1, len(temp_readings)):
        #             readings_list.append(DayForecast(temp_readings[j]))
        #     except:
        #         print("", end="")
        #
        # try:
        #     calculate_results(readings_list, action)
        # except:
        #     print("Invalid file")
        #
        # print("\n\n")
        print("IN AAA")

    if args.a:
        # month, year = get_month(arg_list_row)
        # file_location = ut.get_file_location(year, month, WEATHER_CITY, directory)
        #
        # try:
        #     weather_file = open(file_location, "r")
        #     temp_readings = [line.split(",") for line in weather_file]
        #
        #     for j in range(1, len(temp_readings)):
        #         readings_list.append(DayForecast(temp_readings[j]))
        #
        #     calculate_results(readings_list, action)
        # except:
        #     print("File not found")
        # print("\n\n")
        print("IN AAA")

    if args.c:
        # month, year = get_month(arg_list_row)
        # file_location = ut.get_file_location(year, month, WEATHER_CITY, directory)
        #
        # try:
        #     weather_file = open(file_location, "r")
        #     temp_readings = [line.split(",") for line in weather_file]
        #
        #     for j in range(1, len(temp_readings)):
        #         readings_list.append(DayForecast(temp_readings[j]))
        #
        #     print(month, year)
        #     calculate_results(readings_list, action)
        # except:
        #     print("Invalid file or reading")
        #
        # print("\n\n")

        print("IN CCC")


def calculate_results(yearly_readings, action):
    if action == '-e':
        max_temp_readings = ut.find_max(yearly_readings)  # Max Temperature
        min_temp_readings = ut.find_lowest(yearly_readings)  # Min Temperature
        max_humidity_readings = ut.find_max_humidity(readings_list)  # Max Humidity

        max_temp_month = yearly_readings[max_temp_readings[1]].date
        min_temp_month = yearly_readings[min_temp_readings[1]].date
        max_humidity_month = yearly_readings[max_humidity_readings[1]].date

        max_temp_month_index = int(max_temp_month.split("-")[1]) - 1
        max_temp_day = int(max_temp_month.split("-")[2])

        min_temp_month_index = int(min_temp_month.split("-")[1]) - 1
        min_temp_day = int(min_temp_month.split("-")[2])

        max_humidity_month_index = int(max_humidity_month.split("-")[1]) - 1
        max_humidity_day = int(max_humidity_month.split("-")[2])

        # Displays the reports
        generate_yearly_report(max_temp_readings[0],
                               month_tuple[max_temp_month_index],
                               max_temp_day,
                               min_temp_readings[0],
                               month_tuple[min_temp_month_index],
                               min_temp_day,
                               max_humidity_readings[0],
                               month_tuple[max_humidity_month_index],
                               max_humidity_day)

    elif action == '-a':
        generate_monthly_report(ut.find_avg_highest(yearly_readings),
                                ut.find_avg_lowest(yearly_readings),
                                ut.find_avg_mean_humidity(yearly_readings))

    elif action == '-c':

        for i in range(0, len(yearly_readings)):
            if yearly_readings[i].max_temp != '':
                generate_bar_chart(int(yearly_readings[i].max_temp),
                                   int(yearly_readings[i].min_temp), i + 1)

    yearly_readings.clear()  # Clear the list after generating a report


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


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
