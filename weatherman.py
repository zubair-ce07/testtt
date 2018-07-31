import os
import calendar
import argparse
import csv

data_list_global = []


class Weather:
    date = ''
    max_temp = 0
    min_temp = 0
    max_humidity = 0
    mean_humidity = 0

    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity


class FileParser:
    file_names = []
    data_list = []

    def __init__(self, directory_path):
        file_path = directory_path + '/'
        self.file_names = os.listdir(file_path)
        for j in range(0, len(self.file_names)):
            read_file = csv.DictReader(open("/home/rehan/Documents/task/the-lab/weatherfiles/" + self.file_names[j])
                                       , skipinitialspace=True, delimiter=',')
            for row in read_file:
                if 'PKT' in row:
                    w = Weather(row['PKT'], row['Max TemperatureC'], row['Min TemperatureC'], row['Max Humidity'],
                                row['Mean Humidity'])
                    data_list_global.append(w)
                else:
                    w = Weather(row['PKST'], row['Max TemperatureC'], row['Min TemperatureC'], row['Max Humidity'],
                                row['Mean Humidity'])
                    data_list_global.append(w)


class ResultComputer:
    def give_year_data(self, year):
        highest_temp = 0
        highest_temp_date = 0
        lowest_temp = 100
        lowest_temp_date = 0
        humidity = 0
        humidity_date = 0
        for p in range(0, len(data_list_global)):
            if year == data_list_global[p].date[0:4]:
                if data_list_global[p].max_temp != '':
                    if int(data_list_global[p].max_temp) > highest_temp:
                        highest_temp = int(data_list_global[p].max_temp)
                        highest_temp_date = data_list_global[p].date
                if data_list_global[p].min_temp != '':
                    if int(data_list_global[p].min_temp) < lowest_temp:
                        lowest_temp = int(data_list_global[p].min_temp)
                        lowest_temp_date = data_list_global[p].date
                if data_list_global[p].max_humidity != '':
                    if int(data_list_global[p].max_humidity) > humidity:
                        humidity = int(data_list_global[p].max_humidity)
                        humidity_date = data_list_global[p].date
        return str(highest_temp), calendar.month_name[int(highest_temp_date[5:6])], \
               highest_temp_date[7:], str(lowest_temp), \
               calendar.month_name[int(lowest_temp_date[5:6])], \
               lowest_temp_date[7:], str(humidity), \
               calendar.month_name[int(humidity_date[5:6])], humidity_date[7:]

    def give_month_data(self, year_month):
        highest_cumulative = 0
        highest_counter = 0
        lowest_cumulative = 0
        lowest_counter = 0
        humidity_cumulative = 0
        humidity_counter = 0
        for k in range(0, len(data_list_global)):
            if year_month[0:4] == data_list_global[k].date[0:4] and year_month[-1:] == data_list_global[k].date[5:6]:
                if data_list_global[k].max_temp != '':
                    highest_cumulative = highest_cumulative + int(data_list_global[k].max_temp)
                    highest_counter = highest_counter + 1
                if data_list_global[k].min_temp != '':
                    lowest_cumulative = lowest_cumulative + int(data_list_global[k].min_temp)
                    lowest_counter = lowest_counter + 1
                if data_list_global[k].mean_humidity != '':
                    humidity_cumulative = humidity_cumulative + int(data_list_global[k].mean_humidity)
                    humidity_counter = humidity_counter + 1
        highest_average = int(highest_cumulative / highest_counter)
        lowest_average = int(lowest_cumulative / lowest_counter)
        humidity_average = int(humidity_cumulative / humidity_counter)
        return highest_average, lowest_average, humidity_average


class GenerateReports:

    def generate_average_weather_report(self, highest_average, lowest_average, humidity_average):
        print("Highest Average: " + str(highest_average) + "C")
        print("Lowest Average: " + str(lowest_average) + "C")
        print("Average Mean Humidity: " + str(humidity_average) + "C")

    def generate_extreme_weather_report(self, highest_temp, highest_temp_month, highest_temp_day,
                                        lowest_temp, lowest_temp_month, lowest_temp_day,
                                        humidity, humidity_month, humidity_day):
        print("Highest: " + highest_temp + "C on " + highest_temp_month + " " + highest_temp_day)
        print("Lowest: " + lowest_temp + "C on " + lowest_temp_month + " " + lowest_temp_day)
        print("Humidity: " + humidity + "% on " + humidity_month + " " + humidity_day)

    def generate_extreme_single_bar_report(self, year_month):
        print(calendar.month_name[int(year_month[-1:])] + " " + year_month[:4])
        for k in range(0, len(data_list_global) - 1):
            if year_month[0:4] == data_list_global[k].date[0:4] and year_month[-1:] == data_list_global[k].date[5:6]:
                if data_list_global[k].max_temp != '':
                    print(data_list_global[k].max_temp[7:] + ' ' + '\033[91m' + '+' * int(data_list_global[k].max_temp)
                          + '\033[94m' + '+' * int(data_list_global[k].min_temp) + '\033[0m' +
                          " " + data_list_global[k].max_temp + "C" + " " + data_list_global[k].min_temp + "C")

    def generate_extreme_double_bar_report(self, year_month):
        print(calendar.month_name[int(year_month[-1:])] + " " + year_month[:4])
        for k in range(0, len(data_list_global) - 1):
            if year_month[0:4] == data_list_global[k].date[0:4] and year_month[-1:] == data_list_global[k].date[5:6]:
                if data_list_global[k].max_temp != '':
                    print(data_list_global[k].date[7:] + ' ' + '\033[91m' + '+' * int(data_list_global[k].max_temp) +
                          '\033[0m' + " " + data_list_global[k].max_temp + "C")
                if data_list_global[k].min_temp != '':
                    print(data_list_global[k].date[7:] + ' ' + '\033[94m' + '+' * int(data_list_global[k].min_temp)
                          + '\033[0m' + " " + data_list_global[k].min_temp + "C")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path', help='Insert path of the files')
    parser.add_argument('-e', '--extreme', help='Insert year e.g 2005')
    parser.add_argument('-a', '--average', help='Insert year and month e.g 2006/4')
    parser.add_argument('-c', '--bar', help='Insert year and month e.g 2006/4')
    parser.add_argument('-b', '--bonus', help='Insert year and month e.g 2006/4')
    args = parser.parse_args()

    if not os.path.isdir(args.dir_path):
        print("Error, file path not found")
    else:
        f = FileParser(args.dir_path)

        c = ResultComputer()

        g = GenerateReports()

        if args.extreme:
            highest_temp, highest_temp_month, highest_temp_day, \
            lowest_temp, lowest_temp_month, lowest_temp_day, \
            humidity, humidity_month, humidity_day = c.give_year_data(args.extreme)
            g.generate_extreme_weather_report(highest_temp, highest_temp_month, highest_temp_day,
                                              lowest_temp, lowest_temp_month, lowest_temp_day,
                                              humidity, humidity_month, humidity_day)
        if args.average:
            highest_average, lowest_average, humidity_average = c.give_month_data(args.average)
            g.generate_average_weather_report(highest_average, lowest_average, humidity_average)
        if args.bar:
            g.generate_extreme_double_bar_report(args.bar)
        if args.bonus:
            g.generate_extreme_single_bar_report(args.bonus)


if '__main__' == __name__:
    main()