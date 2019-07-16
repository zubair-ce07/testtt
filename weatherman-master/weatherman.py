import os
import datetime
import argparse

def short_to_long_date(arg):
    date = arg.split("/")
    year, month = date[0], datetime.date(int(date[0]), int(date[1]), 1).strftime('%B')[:3]
    return year, month

class WeathermanEntries(object):

    def __init__(self):
        self.entries = {}

    def set_entries(self, key, entries):
        self.entries[key] = entries

    def highest_temp(self, by=None):
        _highest_temp = 0.0
        _highest_temp_pkt = ''
        found = False
        desired_wmentries = list(filter(lambda x: by in x, self.entries.keys()))
        for entry in desired_wmentries:
            for record in self.entries[entry]:
                max_temp = record.get('Max TemperatureC')
                if max_temp and max_temp.isalnum() and float(max_temp) > _highest_temp:
                    _highest_temp = float(max_temp)
                    _highest_temp_pkt = record.get('PKT') or record.get('PKST')
                    found = True
        if found:
            return _highest_temp, _highest_temp_pkt
        return None, None

    def lowest_temp(self, by=None):
        _lowest_temp = 100
        _lowest_temp_pkt = ''
        found = False
        desired_wmentries = list(filter(lambda x: by in x, self.entries.keys()))
        for entry in desired_wmentries:
            for record in self.entries[entry]:
                min_temp = record.get('Min TemperatureC')
                if min_temp and min_temp.isalnum() and float(min_temp) < _lowest_temp:
                    _lowest_temp = float(min_temp)
                    _lowest_temp_pkt = record.get('PKT') or record.get('PKST')
                    found = True
        if found:
            return _lowest_temp, _lowest_temp_pkt
        return None, None

    def most_humid(self, by=None):
        _most_humid = 0
        _most_humid_pkt = ''
        found = False
        desired_wmentries = list(filter(lambda x: by in x, self.entries.keys()))
        for entry in desired_wmentries:
            for record in self.entries[entry]:
                most_humid = record.get('Max Humidity')
                if most_humid and most_humid.isalnum() and float(most_humid) > _most_humid:
                    _most_humid = float(most_humid)
                    _most_humid_pkt = record.get('PKT') or record.get('PKST')
                    found = True

        if found:
            return _most_humid, _most_humid_pkt
        return None, None

    def highest_avg_temp(self, by=None):
        _highest_temp_avg = 0.0
        found = False
        n = 0
        year, month = short_to_long_date(by)
        desired_wmentries = list(filter(lambda x: by and year in x and month in x, self.entries.keys()))
        for entry in desired_wmentries:
            for record in self.entries[entry]:
                max_temp = record.get('Max TemperatureC')
                if max_temp and max_temp.isalnum():
                    _highest_temp_avg = _highest_temp_avg + float(max_temp)
                    found = True
                    n = n + 1
        if found:
            return float(_highest_temp_avg / float(n))
        return None

    def lowest_avg_temp(self, by=None):
        _lowest_temp_avg = 0.0
        found = False
        n = 0
        year, month = short_to_long_date(by)
        desired_wmentries = list(filter(lambda x: by and year in x and month in x, self.entries.keys()))
        for entry in desired_wmentries:
            for record in self.entries[entry]:
                min_temp = record.get('Min TemperatureC')
                if min_temp and min_temp.isalnum():
                    _lowest_temp_avg = _lowest_temp_avg + float(min_temp)
                    found = True
                    n = n + 1
        if found:
            return float(_lowest_temp_avg / float(n))
        return None

    def avg_mean_humid(self, by=None):
        _mean_humid_avg = 0
        found = False
        n = 0
        year, month = short_to_long_date(by)
        desired_wmentries = list(filter(lambda x: by and year in x and month in x, self.entries.keys()))
        for entry in desired_wmentries:
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
        year, month = short_to_long_date(by)
        desired_wmentries = list(filter(lambda x: by and year in x and month in x, self.entries.keys()))
        for entry in desired_wmentries:
            print("{}, {}".format(month, year))
            for record in self.entries[entry]:
                max_temp = record.get('Max TemperatureC')
                min_temp = record.get('Min TemperatureC')
                if max_temp and min_temp:
                    pkt = record.get("PKT") or record.get("PKST")
                    print(pkt + " \033[91m" + "+" * int(max_temp) + "\033[0m" + " " + max_temp + "C")
                    print(pkt + " \033[34m" + "+" * int(min_temp) + "\033[0m" + " " + min_temp + "C")

    def draw_bonus_chart_for_max_min_temp(self, by=None):
        """ Draw maximum and minimum temperature char for a given year/month"""
        year, month = short_to_long_date(by)
        desired_wmentries = list(filter(lambda x: by and year in x and month in x, self.entries.keys()))
        for entry in desired_wmentries:
            print("{}, {}".format(month, year))
            for record in self.entries[entry]:
                max_temp = record.get('Max TemperatureC')
                min_temp = record.get('Min TemperatureC')
                if max_temp and min_temp:
                    pkt = record.get("PKT") or record.get("PKST")
                    print(pkt + " \033[34m" + "+" * int(min_temp) + "\033[0m" + "\033[91m" + "+" * int(max_temp) + "\033[0m" + " " + min_temp + "C-" + max_temp + "C")

wmentries = WeathermanEntries()


class WeathermanRecord(object):

    def __init__(self, entry):
        self.entry = entry

    def get(self, key):
        return self.entry.get(key, None)

    def __str__(self):
        return str(self.entry)


def read_to_weatherman_entry(meta, line):
    return WeathermanRecord(dict(zip(meta, line)))


def read_parse_file(file):
    f = open(file, "r")
    blank = f.readline()
    meta = f.readline().strip("\n").replace(", ", ",").split(",")
    entries = []
    for line in f.readlines():
        if "<!--" in line:  # skips "<!-- something -->" that occurs at the end of file
            continue
        formatted_line = line.strip("\n").split(",")
        entries.append(read_to_weatherman_entry(meta, formatted_line))
    wmentries.set_entries(file, entries)


def part_one(year):
    highest_temp = wmentries.highest_temp(year)
    lowest_temp = wmentries.lowest_temp(year)
    most_humid = wmentries.most_humid(year)
    print("Highest: {} on {}".format(highest_temp[0], highest_temp[1]))
    print("Lowest: {} on {}".format(lowest_temp[0], lowest_temp[1]))
    print("Humidity: {} on {}".format(most_humid[0], most_humid[1]))


def part_two(date):
    highest_avg_temp = wmentries.highest_avg_temp(date)
    lowest_avg_temp = wmentries.lowest_avg_temp(date)
    avg_mean_humid = wmentries.avg_mean_humid(date)
    print("Highest Average: {}".format(highest_avg_temp) + "C")
    print("Lowest Average: {}".format(lowest_avg_temp) + "C")
    print("Average Mean Humidity: {}".format(avg_mean_humid))


def part_three(date):
    wmentries.draw_chart_for_max_min_temp(date)


def part_four(date):
    wmentries.draw_bonus_chart_for_max_min_temp(date)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='path of directory', type=str)
    parser.add_argument('-m', '--mode', help='path of directory', type=str)
    parser.add_argument('-y', '--year_date_str', type=str, help='path of directory')
    args = parser.parse_args()
    v = vars(args)
    n_args = sum([1 for a in v.values() if a])

    weatherfiles = os.listdir(args.path)
    for file in weatherfiles:
        read_parse_file(os.path.join(args.path, file))

    for i in range(2, ((n_args) + 1), 2):
        if args.mode == '1':
            part_one(args.year_date_str)

        elif args.mode == '2':
                part_two(args.year_date_str)

        elif args.mode == '3':
                part_three(args.year_date_str)

        elif args.mode == '4':
                part_four(args.year_date_str)


main()
