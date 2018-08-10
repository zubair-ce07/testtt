import argparse
import calendar
import csv
import logging
import os
from termcolor import colored


WEATHER_READINGS = []


class Weather:

    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity


class Validator:

    @staticmethod
    def validate_args(argument):
        if len(argument) > 4:
            year_month = argument.split("/")
            month = int(year_month[1])
            if not 1 <= month <= 12:
                raise ValueError("Month has to be between 1 and 12")


class FileParser:

    def parse_files(self, directory_path, argument):
        try:
            Validator.validate_args(argument)
        except:
            logging.error('Invalid argument %s', argument)
            raise
        file_path = directory_path + "/"
        self.file_names = os.listdir(file_path)
        check_file = False
        year = argument.split("/")[0]
        for file_name in self.file_names:
            if year in file_name:
                check_file = True
                read_file = csv.DictReader(open(file_path + file_name), skipinitialspace=True, delimiter=',')
                for row in read_file:
                        weather = Weather(row.get('PKT', row.get('PKST')), row['Max TemperatureC'],
                                          row['Min TemperatureC'], row['Max Humidity'], row['Mean Humidity'])
                        check_item = False
                        for reading in WEATHER_READINGS:
                            if weather.date == reading.date:
                                check_item = True
                        if not check_item:
                            WEATHER_READINGS.append(weather)

        if not check_file:
            raise ValueError("Data for year {} doesn't exist.".format(year))


class ResultComputer:

    def give_year_data(self, year):
        highest_temp = 0
        highest_temp_date = 0
        lowest_temp = 100
        lowest_temp_date = 0
        humidity = 0
        humidity_date = 0
        for reading in WEATHER_READINGS:
            if year == reading.date[0:4] and reading.max_temp != "" and reading.min_temp != "" \
                    and reading.max_humidity != "":
                if int(reading.max_temp) > highest_temp:
                    highest_temp = int(reading.max_temp)
                    highest_temp_date = reading.date.split("-")
                if int(reading.min_temp) < lowest_temp:
                    lowest_temp = int(reading.min_temp)
                    lowest_temp_date = reading.date.split("-")
                if int(reading.max_humidity) > humidity:
                    humidity = int(reading.max_humidity)
                    humidity_date = reading.date.split("-")
        weather_data = {
            "HighestTemp": str(highest_temp),
            "HighestTempMonth": calendar.month_name[int(highest_temp_date[1])],
            "HighestTempDay": highest_temp_date[2],
            "LowestTemp": str(lowest_temp),
            "LowestTempMonth": calendar.month_name[int(lowest_temp_date[1])],
            "LowestTempDay": lowest_temp_date[2],
            "Humidity": str(humidity),
            "HumidityMonth": calendar.month_name[int(humidity_date[1])],
            "HumidityDay": humidity_date[2]
        }
        return weather_data

    def give_month_data(self, year_month):
        year_month = year_month.split("/")
        highest_cumulative = 0
        lowest_cumulative = 0
        humidity_cumulative = 0
        counter = 0
        for reading in WEATHER_READINGS:
            reading_temp = reading.date.split("-")
            if year_month[0] == reading_temp[0] and year_month[1] == reading_temp[1] and reading.max_temp != ""\
                    and reading.min_temp != "" and reading.mean_humidity != "":
                    highest_cumulative = highest_cumulative + int(reading.max_temp)
                    lowest_cumulative = lowest_cumulative + int(reading.min_temp)
                    humidity_cumulative = humidity_cumulative + int(reading.mean_humidity)
                    counter = counter + 1
        highest_average = int(highest_cumulative / counter)
        lowest_average = int(lowest_cumulative / counter)
        humidity_average = int(humidity_cumulative / counter)
        return highest_average, lowest_average, humidity_average


class GenerateReports:

    def generate_average_weather_report(self, highest_average, lowest_average, humidity_average):
        print("Highest Average: {}C".format(highest_average))
        print("Lowest Average: {}C".format(lowest_average))
        print("Average Mean Humidity: {}%".format(humidity_average))

    def generate_extreme_weather_report(self, weather_data):
        print("Highest: {0}C on {1} {2}".format(weather_data['HighestTemp'], weather_data['HighestTempMonth'],
                                                weather_data['HighestTempDay']))
        print("Lowest: {0}C on {1} {2}".format(weather_data['LowestTemp'], weather_data['LowestTempMonth'],
                                               weather_data['LowestTempDay']))
        print("Humidity: {0}% on {1} {2}".format(weather_data['Humidity'], weather_data['HumidityMonth'],
                                                 weather_data['HumidityDay']))

    def generate_extreme_single_bar_report(self, year_month):
        year_month = year_month.split("/")
        print(calendar.month_name[int(year_month[1])] + " " + year_month[0])
        for reading in WEATHER_READINGS:
            date_split = reading.date.split("-")
            if year_month[0] == date_split[0] and year_month[1] == date_split[1] and reading.max_temp != "" \
               and reading.min_temp != "":
                n_plus_signs_red = "+" * int(reading.max_temp)
                plus_sign_red = colored(n_plus_signs_red, 'red')
                n_plus_signs_blue = "+" * int(reading.min_temp)
                plus_sign_blue = colored(n_plus_signs_blue, 'blue')
                print("{0} {1}{2} {3}C {4}C".format(date_split[2], plus_sign_blue, plus_sign_red,
                      reading.max_temp, reading.min_temp))

    def generate_extreme_double_bar_report(self, year_month):
        year_month = year_month.split("/")
        print(calendar.month_name[int(year_month[1])] + " " + year_month[0])
        for reading in WEATHER_READINGS:
            date_split = reading.date.split("-")
            if year_month[0] == date_split[0] and year_month[1] == date_split[1]\
               and reading.max_temp != '' and reading.min_temp != '':
                n_plus_signs_red = "+" * int(reading.max_temp)
                plus_sign_red = colored(n_plus_signs_red, 'red')
                n_plus_signs_blue = "+" * int(reading.min_temp)
                plus_sign_blue = colored(n_plus_signs_blue, 'blue')
                reading_min_temp = colored(reading.min_temp, 'white')
                print("{0} {1} {2}C".format(date_split[2], plus_sign_red, reading.max_temp))
                print("{0} {1} {2}C".format(date_split[2], plus_sign_blue, reading_min_temp))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path', help="Insert path of the files")
    parser.add_argument('-e', '--extreme', help="Insert year e.g 2005 for extreme weather report")
    parser.add_argument('-a', '--average', help="Insert year and month e.g 2006/4 for average weather report")
    parser.add_argument('-c', '--bar', help="Insert year and month e.g 2006/4 for double bar chart report")
    parser.add_argument('-b', '--bonus', help="Insert year and month e.g 2006/4 for single bar chart report")
    args = parser.parse_args()

    if not os.path.isdir(args.dir_path):
        print("Error, file path not found")
    else:
            if args.extreme:
                file_parser = FileParser()
                file_parser.parse_files(args.dir_path, args.extreme)
                result_computer = ResultComputer()
                generate_reports = GenerateReports()
                weather_data = result_computer.give_year_data(args.extreme)
                generate_reports.generate_extreme_weather_report(weather_data)

            if args.average:
                file_parser = FileParser()
                file_parser.parse_files(args.dir_path, args.average)
                result_computer = ResultComputer()
                generate_reports = GenerateReports()
                highest_average, lowest_average, humidity_average = result_computer.give_month_data(args.average)
                generate_reports.generate_average_weather_report(highest_average, lowest_average, humidity_average)

            if args.bar:
                file_parser = FileParser()
                file_parser.parse_files(args.dir_path, args.bar)
                generate_reports = GenerateReports()
                generate_reports.generate_extreme_double_bar_report(args.bar)

            if args.bonus:
                file_parser = FileParser()
                file_parser.parse_files(args.dir_path, args.bonus)
                generate_reports = GenerateReports()
                generate_reports.generate_extreme_single_bar_report(args.bonus)


if '__main__' == __name__:
    main()
