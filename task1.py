import argparse
import calendar
import csv
import os
import pprint
import sys


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
        self.month_to_number = {v: k for k, v in enumerate
        (calendar.month_abbr)}

    def parse_year_data(self, weather_report):

        weather_file_names = [f for f in os.listdir("weatherfiles/weatherfiles/") if
                              f[0] != '.' and f.split('_')[2] == str(args.year)]
        weather_file_names.sort()

        for file in weather_file_names:
            month = self.month_to_number[file.split('_')[-1].split('.')[0]]
            weather_report.update({month: csv.DictReader(open(os.path.join
                                                              ("weatherfiles/weatherfiles/", file)))})

    def parse_month_data(self, weather_report, year_month):
        a = dict((v, k) for k, v in enumerate(calendar.month_abbr))
        month_name = calendar.month_name[int(year_month.split('/')[1])][:3]
        year = str(int(year_month.split('/')[0]))

        Weather_file_names = [f for f in os.listdir("weatherfiles/weatherfiles/") if
                              f[0] != '.' and f.split('_')[-1].split('.')[0] == month_name and
                              f.split('_')[2] == year]

        for file in Weather_file_names:
            month = self.month_to_number[file.split('_')[-1].split('.')[0]]
            weather_report.update({month: csv.DictReader(open(os.path.join
                                                              ("weatherfiles/weatherfiles/", file)))})

class DataResults:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(DataResults, self).__new__(self)

        return self._instance

    def year_report(self, weather_report):
        highest_temp = -9999
        lowest_temp = 9999
        max_humidity = -9999
        highest_temp_date = 0
        lowest_temp_date = 0
        max_humidity_date = 0

        for month in weather_report:
            for date in weather_report[month]:

                if date['Max TemperatureC'] and int(date['Max TemperatureC']) > int(highest_temp):
                    highest_temp = date['Max TemperatureC']
                    highest_temp_date = date['PKT']

                if date['Min TemperatureC'] and int(date['Min TemperatureC']) < int(lowest_temp):
                    lowest_temp = date['Min TemperatureC']
                    lowest_temp_date = date['PKT']

                if date['Max Humidity'] and int(date['Max Humidity']) > int(max_humidity):
                    max_humidity = date['Max Humidity']
                    max_humidity_date = date['PKT']

        return highest_temp, lowest_temp, max_humidity, highest_temp_date, lowest_temp_date, max_humidity_date

    def month_report(self, weather_report):
        temp_count = [0, 0, 0]
        temp_sum = [0, 0, 0]

        for month in weather_report:
            for date in weather_report[month]:

                if date['Max TemperatureC']:
                    temp_count[0] += 1
                    temp_sum[0] += int(date['Max TemperatureC'])

                if date['Min TemperatureC']:
                    temp_count[1] += 1
                    temp_sum[1] += int(date['Min TemperatureC'])

                if date['Max Humidity']:
                    temp_count[2] += 1
                    temp_sum[2] += int(date['Max Humidity'])

            return temp_sum[0] / temp_count[0], temp_sum[1] / temp_count[1], temp_sum[2] / temp_count[2]

    def show_year_result(self, highest_temp, lowest_temp, max_humidity,
                         highest_temp_date, lowest_temp_date, max_humidity_date):

        print("Highest: %s C on %s %s" % (highest_temp,
                                          calendar.month_name[int(highest_temp_date.split('-')[1])],
                                          highest_temp_date.split('-')[2]))

        print("Lowest: %s C on %s %s" % (lowest_temp,
                                         calendar.month_name[int(lowest_temp_date.split('-')[1])],
                                         lowest_temp_date.split('-')[2]))

        print("Humidity: %s per  %s %s" % (max_humidity,
                                           calendar.month_name[int(max_humidity_date.split('-')[1])],
                                           max_humidity_date.split('-')[2]))

    def show_month_result(self, avg_high_temp, avg_low_temp, avg_hum):

        print("Highest Average: %s C" % (str(avg_high_temp)))
        print("Lowest Average: %s C" % (str(avg_low_temp)))
        print("Humidity Average: %s per" % (str(avg_hum)))


class DataReport:
    _instance = None

    def __new__(self):

        if not self._instance:
            self._instance = super(DataReport, self).__new__(self)

        return self._instance

    def show_seprate_graph(self, weather_report):

        for key in weather_report:
            for date in weather_report[key]:
                print(date["PKT"].split('-')[-1], end='')

                if date['Max TemperatureC']:
                    for i in range(0, int(date['Max TemperatureC'])):
                        print(' + ', end='')
                    print("%s C" % date['Max TemperatureC'])
                else:
                    print(" NA")

                print(date['PKT'].split('-')[-1], end='')

                if date['Min TemperatureC']:
                    for j in range(0, int(date['Min TemperatureC'])):
                        print(' - ', end='')
                    print("%s C" % date['Min TemperatureC'])
                else:
                    print(" NA")

        print("\n\n\n")

    def show_merge_graph(self, weather_report):

        for key in weather_report:
            for date in weather_report[key]:
                low = 0
                high = 0
                print(date["PKT"].split('-')[-1], end='')

                if date['Max TemperatureC']:

                    for i in range(0, int(date['Max TemperatureC'])):
                        print(' + ', end='')
                    high = date['Max TemperatureC'] + "C"
                else:
                    print(" NA")

                if date['Min TemperatureC']:

                    for i in range(0, int(date['Min TemperatureC'])):
                        print(' + ', end='')
                    low = (date['Min TemperatureC'] + "C")

                else:
                    print(" NA")

                print("%s-%s" % (high, low))

        print("\n\n\n")


parser = argparse.ArgumentParser(description="Calculating and showing "
                                             "weather reports fetched from the data files")
parser.add_argument("ignore", type=str, help="Directory Destinantion")
parser.add_argument("-e", "--year", type=int, help="Year Parameter")
parser.add_argument("-a", "--month", type=str, help="Month Parameter")
parser.add_argument("-c", "--graphsingle", type=str, help="Show single graph")
parser.add_argument("-m", "--graphmerged", type=str, help="Show merged graph")
args = parser.parse_args()

weather_report = WeatherFilesRecord()
parser = WeatherReportParse()
results = DataResults()

if args.year:
    weather_report = WeatherFilesRecord()
    parser.parse_year_data(weather_report.weather_dic)

    if weather_report.weather_dic:
        highest_temp, lowest_temp, max_humidity, highest_tempDate, lowest_temp_date, max_humidity_date = results.year_report(
            weather_report.weather_dic)
        results.show_year_result(highest_temp, lowest_temp, max_humidity, highest_tempDate, lowest_temp_date,
                                 max_humidity_date)
    else:
        print("%s is not in the record" % args.year)

if args.month:
    weather_report = WeatherFilesRecord()
    parser.parse_month_data(weather_report.weather_dic, args.month)

    if weather_report.weather_dic:
        avg_high_temp, avg_low_temp, avg_hum = results.month_report(weather_report.weather_dic)
        results.show_month_result(avg_high_temp, avg_low_temp, avg_hum)
    else:
        print("%s is not in the record" % args.month)

if args.graphsingle:
    weather_report = WeatherFilesRecord()
    parser.parse_month_data(weather_report.weather_dic, args.graphsingle)

    if weather_report.weather_dic:
        Report = DataReport()
        Report.show_seprate_graph(weather_report.weather_dic)
    else:
        print("%s is not in the record" % args.graphsingle)

if args.graphmerged:
    weather_report = WeatherFilesRecord()
    parser.parse_month_data(weather_report.weather_dic, args.graphmerged)

    if weather_report.weather_dic:
        Report = DataReport()
        Report.show_merge_graph(weather_report.weather_dic)
    else:
        print("%s is not in the record" % args.graphmerged)

