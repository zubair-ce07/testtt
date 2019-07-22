import os
import datetime
import argparse
import csv
import glob

def convert_short_to_long_date(arg):
    date = arg.split("/")
    year, month = date[0], datetime.date(int(date[0]), int(date[1]), 1).strftime('%B')[:3]
    return year, month

class WeathermanEntries(object):

    def __init__(self):
        self.entries = {}

    def set_entries(self, key, entries):
        self.entries[key] = entries

    def calculate_highest_temp(self, by=None):

        _highest_temp = 0.0
        _highest_temp_pkt = ''
        found = False
        desired_weatherman_entries = list(filter(lambda x: by in x, self.entries.keys()))
        for entry in desired_weatherman_entries:
            for record in self.entries[entry]:
                max_temp = record.get('Max TemperatureC')
                if max_temp and max_temp.isalnum() and float(max_temp) > _highest_temp:
                    _highest_temp = float(max_temp)
                    _highest_temp_pkt = record.get('PKT') or record.get('PKST')
                    found = True
        if found:
            return _highest_temp, _highest_temp_pkt
        return None, None

    def calculate_lowest_temp(self, by=None):
        _lowest_temp = 100
        _lowest_temp_pkt = ''
        found = False
        desired_weathermanentries = list(filter(lambda x: by in x, self.entries.keys()))
        for entry in desired_weathermanentries:
            for record in self.entries[entry]:
                min_temp = record.get('Min TemperatureC')
                if min_temp and min_temp.isalnum() and float(min_temp) < _lowest_temp:
                    _lowest_temp = float(min_temp)
                    _lowest_temp_pkt = record.get('PKT') or record.get('PKST')
                    found = True
        if found:
            return _lowest_temp, _lowest_temp_pkt
        return None, None

    def calculate_most_humid(self, by=None):
        _most_humid = 0
        _most_humid_pkt = ''
        found = False
        desired_weathermanentries = list(filter(lambda x: by in x, self.entries.keys()))
        for entry in desired_weathermanentries:
            for record in self.entries[entry]:
                most_humid = record.get('Max Humidity')
                if most_humid and most_humid.isalnum() and float(most_humid) > _most_humid:
                    _most_humid = float(most_humid)
                    _most_humid_pkt = record.get('PKT') or record.get('PKST')
                    found = True

        if found:
            return _most_humid, _most_humid_pkt
        return None, None

    def calculate_highest_avg_temp(self, by=None):
        _highest_temp_avg = 0.0
        found = False
        n = 0
        year, month = convert_short_to_long_date(by)
        desired_weathermanentries = list(filter(lambda x: by and year in x and month in x, self.entries.keys()))
        for entry in desired_weathermanentries:
            for record in self.entries[entry]:
                max_temp = record.get('Max TemperatureC')
                if max_temp and max_temp.isalnum():
                    _highest_temp_avg = _highest_temp_avg + float(max_temp)
                    found = True
                    n = n + 1
        if found:
            return float(_highest_temp_avg / float(n))
        return None

    def calculate_lowest_avg_temp(self, by=None):
        _lowest_temp_avg = 0.0
        found = False
        n = 0
        year, month = convert_short_to_long_date(by)
        desired_weatherman_entries = list(filter(lambda x: by and year in x and month in x, self.entries.keys()))
        for entry in desired_weatherman_entries:
            for record in self.entries[entry]:
                min_temp = record.get('Min TemperatureC')
                if min_temp and min_temp.isalnum():
                    _lowest_temp_avg = _lowest_temp_avg + float(min_temp)
                    found = True
                    n = n + 1
        if found:
            return float(_lowest_temp_avg / float(n))
        return None

    def calculate_avg_mean_humid(self, by=None):
        _mean_humid_avg = 0
        found = False
        n = 0
        year, month = convert_short_to_long_date(by)
        desired_weatherman_entries = list(filter(lambda x: by and year in x and month in x, self.entries.keys()))
        for entry in desired_weatherman_entries:
            for record in self.entries[entry]:
                mean_humid = record.get('Mean Humidity')
                if mean_humid and mean_humid.isalnum():
                    _mean_humid_avg = _mean_humid_avg + float(mean_humid)
                    found = True
                    n = n + 1

        if found:
            return _mean_humid_avg
        return None

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
                    print(pkt + " \033[34m" + "+" * int(min_temp) + "\033[0m" + "\033[91m" + "+" * int(max_temp) + "\033[0m" + " " + min_temp + "C-" + max_temp + "C")

weatherman_entries = WeathermanEntries()


class WeathermanRecord(object):

    def __init__(self, entry):
        self.entry = entry

    def get(self, key):
        return self.entry.get(key, None)

    def __str__(self):
        return str(self.entry)


def read_to_weatherman_entry(meta, line):
    return WeathermanRecord(dict(zip(meta, line)))


def read_parse_file(csv_path):
    with open(csv_path) as input_file:
        weather_reader = csv.DictReader(input_file)
        weather_reader_list = list(weather_reader)
        return weather_reader_list

def calculate_highest_and_lowest_temperature_and_humidity_of_given_year(year):
    highest_temp = weatherman_entries.calculate_highest_temp(year)
    lowest_temp = weatherman_entries.calculate_lowest_temp(year)
    most_humid = weatherman_entries.calculate_most_humid(year)
    return highest_temp, lowest_temp, most_humid

def report_highest_and_lowest_temperature_and_humidity_of_given_year(highest_temp, lowest_temp, most_humid):
    print("Highest: {} on {}".format(highest_temp[0], highest_temp[1]))
    print("Lowest: {} on {}".format(lowest_temp[0], lowest_temp[1]))
    print("Humidity: {} on {}".format(most_humid[0], most_humid[1]))

def calculate_highest_and_lowest_temperature_and_humidity_of_given_month_of_year(date):
    highest_avg_temp = weatherman_entries.calculate_highest_avg_temp(date)
    lowest_avg_temp = weatherman_entries.calculate_lowest_avg_temp(date)
    avg_mean_humid = weatherman_entries.calculate_avg_mean_humid(date)
    return highest_avg_temp, lowest_avg_temp, avg_mean_humid

def report_highest_and_lowest_temperature_and_humidity_of_given_month_of_year(highest_avg_temp, lowest_avg_temp, avg_mean_humid):

    print("Highest Average: {}".format(highest_avg_temp) + "C")
    print("Lowest Average: {}".format(lowest_avg_temp) + "C")
    print("Average Mean Humidity: {}".format(avg_mean_humid))


def draw_two_line_horizontal_bar_chart(date):
    weatherman_entries.draw_chart_for_max_min_temp(date)


def draw_one_line_horizontal_bar_chart(date):
    weatherman_entries.draw_bonus_chart_for_max_min_temp(date)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path of directory')
    parser.add_argument('-e', dest='year_to_report', action='store')
    parser.add_argument('-a', dest='month_to_report', action='store')
    parser.add_argument('-c', dest='plot_graph', action='store')
    parser.add_argument('year_date', help='path of directory')

    args = parser.parse_args()
    arguments = vars(args)
    no_of_args = sum([1 for a in arguments.values() if a])

    for file in glob.glob("*" + args.path + "/*.txt"):
        read_parse_file(file)

    for i in range(2, ((no_of_args) + 1), 2):
        if  args.year_to_report:
                highest_temp, lowest_temp, most_humid= calculate_highest_and_lowest_temperature_and_humidity_of_given_year(args.year_date)
                report_highest_and_lowest_temperature_and_humidity_of_given_year(highest_temp, lowest_temp, most_humid)

        elif args.month_to_report:
                avg_highest_temp, avg_lowest_temp, avg_most_humid= calculate_highest_and_lowest_temperature_and_humidity_of_given_month_of_year(args.year_date)
                report_highest_and_lowest_temperature_and_humidity_of_given_month_of_year(avg_highest_temp, avg_lowest_temp, avg_most_humid)
        elif args.plot_graph:
                draw_two_line_horizontal_bar_chart(args.year_date)
                draw_one_line_horizontal_bar_chart(args.year_date)

if __name__ == "__main__":
    main()

