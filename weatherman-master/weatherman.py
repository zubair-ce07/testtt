import os
import datetime
import argparse
import csv
import glob
from operator import attrgetter

def convert_short_to_long_date(arg):

    date = arg.split("/")
    year, month = date[0], datetime.date(int(date[0]), int(date[1]), 1).strftime('%B')[:3]
    return year, month

class WeathermanEntries(object):

    def __init__(self, weather_timezone, max_temperature, min_temperature, max_humidity, average_humididty):
        self.weather_timezone = weather_timezone
        self.max_temperature = int(max_temperature) if max_temperature else 0
        self.min_temperature = int(min_temperature) if min_temperature else 0
        self.max_humidity = int(max_humidity) if max_humidity else 0
        self.average_humididty = int(average_humididty) if average_humididty else 0

    def calculate_highest_temp(weatherman_entries):

        return max(weatherman_entries, key=attrgetter('max_temperature')),

    def calculate_lowest_temp(weatherman_entries):

        return min(weatherman_entries, key=attrgetter('min_temperature')),

    def calculate_most_humid(weatherman_entries):

        return max(weatherman_entries, key=attrgetter('max_humidity'))

    def calculate_highest_avg_temp(weatherman_entries):

        temperature_count = len(weatherman_entries)
        highest_temperature_value = round(sum(weatherman.max_temperature for weatherman
        in weatherman_entries)/ temperature_count, 2)
        return highest_temperature_value

    def calculate_lowest_avg_temp(weatherman_entries):

        temperature_count = len(weatherman_entries)
        lowest_temperature_value = round(sum(weatherman.max_temperature for weatherman
        in weatherman_entries)/ temperature_count, 2)
        return lowest_temperature_value

    def calculate_avg_mean_humid(self, by=None):

        temperature_count = len(weatherman_entries)
        average_humidity_value = round(sum(weatherman.average_humididty for weatherman
        in weatherman_entries)/ temperature_count, 2)
        return average_humidity_value

    def draw_chart_for_max_min_temp(self, by=None):

        year, month = convert_short_to_long_date(by)
        desired_weatherman_entries = list(filter(lambda x: by and year in x and month in x, self.entries.keys()))
        for entry in desired_weatherman_entries:
            print("{}, {}".format(month, year))
            for record in self.entries[entry]:
                max_temp = record.get('Max TemperatureC')
                min_temp = record.get('Min TemperatureC')
                if max_temp and min_temp:
                    pkt = record.get("PKT") or record.get("PKST")
                    print(pkt + " \033[91m" + "+" * int(max_temp) + "\033[0m" + " " + max_temp + "C")
                    print(pkt + " \033[34m" + "+" * int(min_temp) + "\033[0m" + " " + min_temp + "C")

    def draw_bonus_chart_for_max_min_temp(self, by=None):

        year, month = convert_short_to_long_date(by)
        desired_weatherman_entries = list(filter(lambda x: by and year in x and month in x, self.entries.keys()))
        for entry in desired_weatherman_entries:
            print("{}, {}".format(month, year))
            for record in self.entries[entry]:
                max_temp = record.get('Max TemperatureC')
                min_temp = record.get('Min TemperatureC')
                if max_temp and min_temp:
                    pkt = record.get("PKT") or record.get("PKST")
                    print(pkt + " \033[34m" + "+" * int(min_temp) + "\033[0m" + "\033[91m" + "+" * int(max_temp)
                          + "\033[0m" + " " + min_temp + "C-" + max_temp + "C")

weatherman_entries = WeathermanEntries()

class WeathermanRecord(object):

    def read_to_weatherman_entry(meta, line):
        
        return WeathermanRecord(dict(zip(meta, line)))

def read_parse_report(csv_path):

    with open(csv_path) as input_file:
        weather_reader = csv.DictReader(input_file)
        weather_reader_list = list(weather_reader)
        return weather_reader_list

def calculate_given_year_temperature(year):

    highest_temp = weatherman_entries.calculate_highest_temp(year)
    lowest_temp = weatherman_entries.calculate_lowest_temp(year)
    most_humid = weatherman_entries.calculate_most_humid(year)
    return highest_temp, lowest_temp, most_humid

def report_given_year_temperature(highest_temp, lowest_temp, most_humid):

    print("Highest: {} on {}".format(highest_temp[0], highest_temp[1]))
    print("Lowest: {} on {}".format(lowest_temp[0], lowest_temp[1]))
    print("Humidity: {} on {}".format(most_humid[0], most_humid[1]))

def calculate_given_month_temperature(date):

    highest_avg_temp = weatherman_entries.calculate_highest_avg_temp(date)
    lowest_avg_temp = weatherman_entries.calculate_lowest_avg_temp(date)
    avg_mean_humid = weatherman_entries.calculate_avg_mean_humid(date)
    return highest_avg_temp, lowest_avg_temp, avg_mean_humid

def report_given_month_temperature(highest_avg_temp, lowest_avg_temp, avg_mean_humid):

    print("Highest Average: {}".format(highest_avg_temp) + "C")
    print("Lowest Average: {}".format(lowest_avg_temp) + "C")
    print("Average Mean Humidity: {}".format(avg_mean_humid))

def draw_two_line_horizontal_bar_chart(date):
    weatherman_entries.draw_chart_for_max_min_temp(date)

def draw_one_line_horizontal_bar_chart(date):
    weatherman_entries.draw_bonus_chart_for_max_min_temp(date)

def main():

    weather_mans = []
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path of directory')
    parser.add_argument('-e', '--year_date', nargs='*', dest='year_to_report', action='store',
                        type=lambda date_in_string: datetime.strptime(date_in_string, '%Y').date())
    parser.add_argument('-a', '--year_date', nargs='*', dest='month_to_report', action='store',
                        type=lambda date_in_string: datetime.strptime(date_in_string, '%Y/%m').date())
    parser.add_argument('-c', '--year_date', nargs='*', dest='plot_graph', action='store',
                        type=lambda date_in_string: datetime.strptime(date_in_string, '%Y/%m').date())
    args = parser.parse_args()
    for report in glob.glob("*" + args.path + "/*.txt"):
        read_parse_report(report)

    if args.year_date:
        if  args.year_to_report:
                highest_temp, lowest_temp, most_humid= calculate_given_year_temperature(args.year_date)
                report_given_year_temperature(highest_temp, lowest_temp, most_humid)

        elif args.month_to_report:
                avg_highest_temp, avg_lowest_temp, avg_most_humid= calculate_given_month_temperature(args.year_date)
                report_given_month_temperature(avg_highest_temp, avg_lowest_temp, avg_most_humid)

        elif args.plot_graph:
                draw_two_line_horizontal_bar_chart(args.year_date)
                draw_one_line_horizontal_bar_chart(args.year_date)

if __name__ == "__main__":
    main()

