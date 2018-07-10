import calendar as cal
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


def get_month(string):
    return string[:3]


def get_year(action):
    year = 0
    for i in action or []:
        year = i
    return year


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

    # Reading all the files in the directory
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
    print("\n")


def calculate_results(args, readings):
    list_subset = []
    if args.e:
        year = get_year(args.e)
        for i in readings:
            if year in i.date and not (i.max_temp == ''
                                       and i.min_temp == ''
                                       and i.max_humidity == ''):
                list_subset.append(i)

        node_max = max(list_subset, key=lambda DayForecast: int(DayForecast.max_temp))
        node_min = min(list_subset, key=lambda DayForecast: int(DayForecast.min_temp))
        node_max_humidity = max(list_subset, key=lambda DayForecast: int(DayForecast.max_humidity))

        generate_yearly_report(node_max, node_min, node_max_humidity)
        list_subset.clear()

    if args.a:
        temp = get_year(args.a).split("/")
        key = temp[0] + "-" + temp[1]

        for i in readings:
            if key in i.date and not (i.max_temp == ''
                                      and i.min_temp == ''
                                      and i.mean_humidity == ''):
                list_subset.append(i)

        avg_max_temp = round(sum(int(DayForecast.max_temp) for DayForecast in list_subset) / len(list_subset))
        avg_min_temp = round(sum(int(DayForecast.min_temp) for DayForecast in list_subset) / len(list_subset))
        avg_mean_humidity = round(sum(int(DayForecast.mean_humidity) for DayForecast in list_subset) / len(list_subset))

        generate_monthly_report(avg_max_temp, avg_min_temp, avg_mean_humidity)
        list_subset.clear()

    if args.c:
        day_index = 1
        temp = get_year(args.c).split("/")
        key = temp[0] + "-" + temp[1][1:]

        print(cal.month_name[int(temp[1])], temp[0])
        for i in readings:
            if key in i.date and not (i.max_temp == ''
                                      and i.min_temp == ''
                                      and i.mean_humidity == ''):

                # UNCOMMENT ONE OF ANY BAR CHART FORMATS
                display_single_bar_chart(day_index, i.min_temp, i.max_temp)
                # display_separate_bar_charts(day_index, i.min_temp, i.max_temp)

                day_index += 1


def display_single_bar_chart(day, min_temp, max_temp):
    print("%d " % day, end="")
    ut.print_blue("+", int(min_temp))
    ut.print_red("+", int(max_temp))
    print(" %sC - %sC" % (min_temp, max_temp))


def display_separate_bar_charts(day, min_temp, max_temp):
    print("%d " % day, end="")
    ut.print_red("+", int(max_temp))
    print(" %sC" % max_temp)

    print("%d " % day, end="")
    ut.print_blue("+", int(min_temp))
    print(" %sC" % min_temp)


def get_date_params(string):
    string = string.split("-")
    return [string[0], string[1], string[2]]


def generate_yearly_report(max_node, min_node, humidity_node):
    year_max, month_max, date_max = get_date_params(max_node.date)
    year_min, month_min, date_min = get_date_params(min_node.date)
    year_humid, month_humid, date_humid = get_date_params(humidity_node.date)

    print("Highest: %sC on %s %s" % (max_node.max_temp, cal.month_name[int(month_max)], date_max))
    print("Lowest: %sC on %s %s" % (min_node.min_temp, cal.month_name[int(month_min)], date_min))
    print("Humidity: %s%% on %s %s" % (humidity_node.max_humidity, cal.month_name[int(month_humid)], date_humid))
    print('\n')


def generate_monthly_report(avg_max_temp, avg_lowest_temp, avg_mean_humidity):
    print("Highest Average: %dC" % avg_max_temp)
    print("Lowest Average: %dC" % avg_lowest_temp)
    print("Average Mean Humidity: %d%%" % avg_mean_humidity)
    print('\n')


def main(arguments):
    readings_list = []
    parse_files(arguments.directory, readings_list)
    calculate_results(arguments, readings_list)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
