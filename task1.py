import argparse
import calendar
import csv
import os
import pprint
import sys


class CleanData:
    def __init__(self, date, max_temp, min_temp, max_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity


class WeatherFilesRecord:
    def __init__(self):
        self.weather_dic = {}


class WeatherReportParse:
    _instance = None

    def __new__(self):

        if not self._instance:
            self._instance = super(WeatherReportParse, self).__new__(self)

        return self._instance

    def __init__(self):
        self.month_to_number = {v: k for k, v in enumerate(calendar.month_abbr)}

    def parse_year_data(self, weather_report):

        weather_file_names = [f for f in os.listdir(args.path) if
                              f[0] != '.' and f.split('_')[2] == str(args.year)]
        weather_file_names.sort()

        for weather_file in weather_file_names:
            month = self.month_to_number[weather_file.split('_')[-1].split('.')[0]]
            weather_report.update({month: csv.DictReader(open(os.path.join
                                                              (args.path, weather_file)))})

    def parse_month_data(self, weather_report, year_month):
        a = dict((v, k) for k, v in enumerate(calendar.month_abbr))
        month_name = calendar.month_name[int(year_month.split('/')[1])][:3]
        year = str(int(year_month.split('/')[0]))

        Weather_file_names = [f for f in os.listdir(args.path) if
                              f[0] != '.' and f.split('_')[-1].split('.')[0] == month_name and
                              f.split('_')[2] == year]

        for weather_file in Weather_file_names:
            month = self.month_to_number[weather_file.split('_')[-1].split('.')[0]]
            weather_report.update({month: csv.DictReader(open(os.path.join
                                                              (args.path, weather_file)))})


class DataResults:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(DataResults, self).__new__(self)

        return self._instance

    def year_report(self, clean_data):
        highest_temp = max(clean_data, key=lambda x: int(x.max_temp))
        lowest_temp = min(clean_data, key=lambda x: int(x.min_temp))
        max_humidity = max(clean_data, key=lambda x: int(x.max_humidity))

        return highest_temp, lowest_temp, max_humidity

    def month_report(self, clean_data):
        temp_count = [0, 0, 0]
        temp_sum = [0, 0, 0]

        for weather_record in clean_data:
            temp_count[0] += 1
            temp_sum[0] += int(weather_record.max_temp)

            temp_count[1] += 1
            temp_sum[1] += int(weather_record.min_temp)

            temp_count[2] += 1
            temp_sum[2] += int(weather_record.max_humidity)

        return temp_sum[0] / temp_count[0], temp_sum[1] / temp_count[1], temp_sum[2] / temp_count[2]

    def show_year_result(self, highest_temp, lowest_temp, max_humidity):
        month_name = calendar.month_name[int(highest_temp.date.split('-')[1])]
        temp = highest_temp.date.split('-')[2]
        print(f'Highest: {highest_temp.max_temp} C on {month_name} {temp}')

        month_name = calendar.month_name[int(lowest_temp.date.split('-')[1])]
        temp = lowest_temp.date.split('-')[2]
        print(f'Lowest: {lowest_temp.min_temp} C on {month_name} {temp}')

        month_name = calendar.month_name[int(max_humidity.date.split('-')[1])]
        temp = max_humidity.date.split('-')[2]
        print(f'Humidity: {max_humidity.max_humidity} C on {month_name} {temp}')

    def show_month_result(self, avg_high_temp, avg_low_temp, avg_hum):

        print(f'Highest Average: {avg_high_temp} C')
        print(f'Lowest Average: {avg_low_temp} C')
        print(f'Humidity Average: {avg_hum} per')


class DataReport:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(DataReport, self).__new__(self)

        return self._instance

    def show_seprate_graph(self, clean_data):
        for weather_date in weather_report:
            print(weather_date.date.split('-')[-1], end='')

            for i in range(0, int(weather_date.max_temp)):
                print(' + ', end='')

            print("%s C" % weather_date.max_temp)
            print(weather_date.date.split('-')[-1], end='')

            for j in range(0, int(weather_date.min_temp)):
                print(' - ', end='')
            print("%s C" % weather_date.min_temp)

        print("\n\n\n")

    def show_merge_graph(self, weather_report):
        for weather_date in weather_report:
            low = 0
            high = 0
            print(weather_date.date.split('-')[-1], end='')

            for i in range(0, int(weather_date.max_temp)):
                print(' + ', end='')
            high = weather_date.max_temp + "C"

            for i in range(0, int(weather_date.min_temp)):
                print(' + ', end='')
            low = (weather_date.min_temp + "C")

            print("%s-%s" % (high, low))


def fetch_clean_data(clean_data, weather_report):
    for weather_month in weather_report.weather_dic:
        for weather_date in weather_report.weather_dic[weather_month]:
            if weather_date['Max TemperatureC']:
                clean_data.append(CleanData(weather_date['PKT'],
                                            weather_date['Max TemperatureC'],
                                            weather_date['Min TemperatureC'],
                                            weather_date['Max Humidity']))


def check_data_validation(weather_report):
    if not weather_report:
        print(f'{args.year} is not in the record')
        return 0
    else:
        return 1


parser = argparse.ArgumentParser(description="Calculating and showing "
                                             "weather reports fetched from the data files")
parser.add_argument("path", type=str, help="Directory Destinantion")
parser.add_argument("-e", "--year", type=int, help="Year Parameter")
parser.add_argument("-a", "--month", type=str, help="Month Parameter")
parser.add_argument("-c", "--graphsingle", type=str, help="Show single graph")
parser.add_argument("-m", "--graphmerged", type=str, help="Show merged graph")
args = parser.parse_args()

weather_report = WeatherFilesRecord()
parser = WeatherReportParse()
results = DataResults()
clean_data = []

if args.year:
    weather_report = WeatherFilesRecord()
    parser.parse_year_data(weather_report.weather_dic)

    if check_data_validation(weather_report.weather_dic):
        fetch_clean_data(clean_data, weather_report)
        highest_temp, lowest_temp, max_humidity = results.year_report(clean_data)
        results.show_year_result(highest_temp, lowest_temp, max_humidity)

if args.month:
    weather_report = WeatherFilesRecord()
    parser.parse_month_data(weather_report.weather_dic, args.month)

    if check_data_validation(weather_report.weather_dic):
        fetch_clean_data(clean_data, weather_report)
        avg_high_temp, avg_low_temp, avg_hum = results.month_report(clean_data)
        results.show_month_result(avg_high_temp, avg_low_temp, avg_hum)

if args.graphsingle:
    weather_report = WeatherFilesRecord()
    parser.parse_month_data(weather_report.weather_dic, args.graphsingle)

    if check_data_validation(weather_report.weather_dic):
        fetch_clean_data(clean_data, weather_report)
        Report = DataReport()
        Report.show_seprate_graph(clean_data)

if args.graphmerged:
    weather_report = WeatherFilesRecord()
    parser.parse_month_data(weather_report.weather_dic, args.graphmerged)

    if check_data_validation(weather_report.weather_dic):
        fetch_clean_data(clean_data, weather_report)
        Report = DataReport()
        Report.show_merge_graph(clean_data)

