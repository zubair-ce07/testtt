import argparse
import calendar
import csv
import os
import sys
from termcolor import colored


WEATHER_READINGS = []


class Weather:
    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity


class FileParser:
    def __init__(self, directory_path):
        file_path = directory_path + '/'
        self.file_names = os.listdir(file_path)
        for file in self.file_names:
            read_file = csv.DictReader(open(file_path + file)
                                       , skipinitialspace=True, delimiter=',')
            for row in read_file:
                    weather = Weather(row.get("PKT", "PKST"), row['Max TemperatureC'], row['Min TemperatureC'],
                                      row['Max Humidity'], row['Mean Humidity'])
                    WEATHER_READINGS.append(weather)


class ResultComputer:
    @staticmethod
    def give_year_data(year):
        highest_temp = 0
        highest_temp_date = 0
        lowest_temp = 100
        lowest_temp_date = 0
        humidity = 0
        humidity_date = 0
        for reading in WEATHER_READINGS:
            if year == reading.date[0:4] and reading.max_temp != '' and reading.min_temp != '' \
                    and reading.max_humidity != '':
                    if int(reading.max_temp) > highest_temp:
                        highest_temp = int(reading.max_temp)
                        highest_temp_date = reading.date
                    if int(reading.min_temp) < lowest_temp:
                        lowest_temp = int(reading.min_temp)
                        lowest_temp_date = reading.date
                    if int(reading.max_humidity) > humidity:
                        humidity = int(reading.max_humidity)
                        humidity_date = reading.date
        weather_data = {
            "HighestTemp": str(highest_temp),
            "HighestTempMonth": calendar.month_name[int(highest_temp_date[5:6])],
            "HighestTempDay": highest_temp_date[7:],
            "LowestTemp": str(lowest_temp),
            "LowestTempMonth": calendar.month_name[int(lowest_temp_date[5:6])],
            "LowestTempDay": lowest_temp_date[7:],
            "Humidity": str(humidity),
            "HumidityMonth": calendar.month_name[int(humidity_date[5:6])],
            "HumidityDay": humidity_date[7:]
        }
        return weather_data

    @staticmethod
    def give_month_data(year_month):
        highest_cumulative = 0
        highest_counter = 0
        lowest_cumulative = 0
        lowest_counter = 0
        humidity_cumulative = 0
        humidity_counter = 0
        for reading in WEATHER_READINGS:
            if year_month[0:4] == reading.date[0:4] and year_month[-1:] == reading.date[5:6] and reading.max_temp != ''\
                    and reading.min_temp != '' and reading.mean_humidity != '':
                    highest_cumulative = highest_cumulative + int(reading.max_temp)
                    highest_counter = highest_counter + 1
                    lowest_cumulative = lowest_cumulative + int(reading.min_temp)
                    lowest_counter = lowest_counter + 1
                    humidity_cumulative = humidity_cumulative + int(reading.mean_humidity)
                    humidity_counter = humidity_counter + 1
        highest_average = int(highest_cumulative / highest_counter)
        lowest_average = int(lowest_cumulative / lowest_counter)
        humidity_average = int(humidity_cumulative / humidity_counter)
        return highest_average, lowest_average, humidity_average


class GenerateReports:
    @staticmethod
    def generate_average_weather_report(highest_average, lowest_average, humidity_average):
        print("Highest Average: {}C".format(highest_average))
        print("Lowest Average: {}C".format(lowest_average))
        print("Average Mean Humidity: {}C".format(humidity_average))

    @staticmethod
    def generate_extreme_weather_report(highest_temp, highest_temp_month, highest_temp_day,
                                        lowest_temp, lowest_temp_month, lowest_temp_day,
                                        humidity, humidity_month, humidity_day):
        print("Highest: {0}C on {1} {2}".format(highest_temp, highest_temp_month, highest_temp_day))
        print("Lowest: {0}C on {1} {2}".format(lowest_temp, lowest_temp_month, lowest_temp_day))
        print("Humidity: {0}C on {1} {2}".format(humidity, humidity_month, humidity_day))

    @staticmethod
    def generate_extreme_weather_report(weather_data):
        print("Highest: {0}C on {1} {2}".format(weather_data["HighestTemp"], weather_data["HighestTempMonth"],
                                                weather_data["HighestTempDay"]))
        print("Lowest: {0}C on {1} {2}".format(weather_data["LowestTemp"], weather_data["LowestTempMonth"],
                                               weather_data["LowestTempDay"]))
        print("Humidity: {0}C on {1} {2}".format(weather_data["Humidity"], weather_data["HumidityMonth"],
                                                 weather_data["HumidityDay"]))

    @staticmethod
    def generate_extreme_single_bar_report(year_month):
        plus_sign_red = colored("+", 'red')
        plus_sign_blue = colored("+", 'blue')
        print(calendar.month_name[int(year_month[-1:])] + " " + year_month[:4])
        for reading in WEATHER_READINGS:
            if year_month[0:4] == reading.date[0:4] and year_month[-1:] == reading.date[5:6] and reading.max_temp != '':
                    print(reading.max_temp[7:] + ' ' + plus_sign_blue * int(reading.max_temp)
                          + plus_sign_red * int(reading.min_temp) + " " + reading.max_temp + "C" + " "
                          + reading.min_temp + "C")

    @staticmethod
    def generate_extreme_double_bar_report(year_month):
        plus_sign_red = colored("+", 'red')
        plus_sign_blue = colored("+", 'blue')
        print(calendar.month_name[int(year_month[-1:])] + " " + year_month[:4])
        for reading in WEATHER_READINGS:
            if year_month[0:4] == reading.date[0:4] and year_month[-1:] == reading.date[5:6]\
            and reading.max_temp != '' and reading.min_temp != '':
                    print(reading.date[7:] + ' ' + plus_sign_blue * int(reading.max_temp) + " " +
                          reading.max_temp + "C")
                    print(reading.date[7:] + ' ' + plus_sign_red * int(reading.min_temp) + " " + reading.min_temp + "C")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path', help='Insert path of the files')
    parser.add_argument('-e', '--extreme', help='Insert year e.g 2005 for extreme weather report')
    parser.add_argument('-a', '--average', help='Insert year and month e.g 2006/4 for average weather report')
    parser.add_argument('-c', '--bar', help='Insert year and month e.g 2006/4 for double bar chart report')
    parser.add_argument('-b', '--bonus', help='Insert year and month e.g 2006/4 for single bar chart report')
    args = parser.parse_args()

    if not os.path.isdir(args.dir_path):
        print("Error, file path not found")
    else:
        file_parser = FileParser(args.dir_path)

        result_computer = ResultComputer()

        generate_reports = GenerateReports()

        if args.extreme:
            weather_data = result_computer.give_year_data(args.extreme)
            generate_reports.generate_extreme_weather_report(weather_data)
        if args.average:
            highest_average, lowest_average, humidity_average = result_computer.give_month_data(args.average)
            generate_reports.generate_average_weather_report(highest_average, lowest_average, humidity_average)
        if args.bar:
            generate_reports.generate_extreme_double_bar_report(args.bar)
        if args.bonus:
            generate_reports.generate_extreme_single_bar_report(args.bonus)


if '__main__' == __name__:
    main()
