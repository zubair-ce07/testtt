import argparse
import calendar
import csv
from datetime import datetime
import glob
import os
import pprint
import sys


class CleanWeatherRecord:
    def __init__(self, date, max_temp, min_temp, max_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity


class WeatherReportParse:
    _instance = None

    def __new__(self):

        if not self._instance:
            self._instance = super(WeatherReportParse, self).__new__(self)

        return self._instance

    def __init__(self):
        self.month_to_number = {v: k for k, v in enumerate(calendar.month_abbr)}

    def get_file_names(self, path, date_object):

        if str(type(date_object)) == '<class \'datetime.datetime\'>':
            files_names = glob.glob(
                "{}/Murree_weather_{}_{}.txt".format(path, date_object.strftime("%Y"), date_object.strftime("%b")))
        else:
            files_names = glob.glob("{}/Murree_weather_{}_*.txt".format(path, date_object))

        return [x[18:] for x in files_names]

    def read_files_record(self, weather_file_names, path):
        clean_data = []
        for weather_file in weather_file_names:
            file_data = csv.DictReader(open(os.path.join(path, weather_file)))
            # file_keys = [x2[0] for x2 in list(list(file_data)[0].items())]

            for weather_date in file_data:
                if weather_date["Max TemperatureC"] and weather_date["Min TemperatureC"] and \
                        weather_date["Max Humidity"]:
                    clean_data.append(CleanWeatherRecord(weather_date["PKT"],
                                                         weather_date["Max TemperatureC"],
                                                         weather_date["Min TemperatureC"],
                                                         weather_date["Max Humidity"]))
        return clean_data

    def parse_weather_data(self, path, year_month):
        weather_file_names = self.get_file_names(path, year_month)
        return self.read_files_record(weather_file_names, path)


class ShowWeatherResults():
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(ShowWeatherResults, self).__new__(self)

        return self._instance

    def show_extreme_result(self, highest_temp, lowest_temp, max_humidity):
        date_object = datetime.strptime(highest_temp.date, "%Y-%m-%d")
        print("Highest: {} C on {} {}".format(highest_temp.max_temp, date_object.strftime("%b"),
                                              date_object.strftime("%d")))

        date_object = datetime.strptime(lowest_temp.date, "%Y-%m-%d")
        print("Lowest: {} C on {} {}".format(lowest_temp.min_temp, date_object.strftime("%b"),
                                             date_object.strftime("%d")))

        date_object = datetime.strptime(max_humidity.date, "%Y-%m-%d")
        print("Humidity: {} C on {} {}".format(max_humidity.max_humidity, date_object.strftime("%b"),
                                               date_object.strftime("%d")))

    def show_average_result(self, avg_high_temp, avg_low_temp, avg_hum):
        print("Highest Average: {} C".format(avg_high_temp))
        print("Lowest Average: {} C".format(avg_low_temp))
        print("Humidity Average: {} per".format(avg_hum))

    def show_seprate_chart(self, clean_data):
        for weather_date in clean_data:
            date_object = datetime.strptime(weather_date.date, "%Y-%m-%d")
            print(date_object.strftime("%d"), end="")

            for i in range(0, int(weather_date.max_temp)):
                print("\033[1;31;40m + ", end="")

            print("{} C".format(weather_date.max_temp))
            print(date_object.strftime("%d"), end="")

            for j in range(0, int(weather_date.min_temp)):
                print("\033[1;34;40m - ", end="")
            print("{} C".format(weather_date.min_temp))

    def show_merge_chart(self, weather_report):
        for weather_date in weather_report:
            date_object = datetime.strptime(weather_date.date, "%Y-%m-%d")
            print("\033[1;31;40m {}".format(date_object.strftime("%d")), end="\t")
            print("\033[1;31;40m {} C".format(weather_date.max_temp), end="")

            for i in range(0, int(weather_date.max_temp)):
                print("\033[1;31;40m + ", end="")

            for j in range(0, int(weather_date.min_temp)):
                print("\033[1;34;40m + ", end="")

            print("\033[1;34;40m {} C".format(weather_date.min_temp))


class CalculateWeatherResults:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(CalculateWeatherResults, self).__new__(self)

        return self._instance

    def calculate_extreme_report(self, clean_data):
        highest_temp = max(clean_data, key=lambda x: int(x.max_temp))
        lowest_temp = min(clean_data, key=lambda x: int(x.min_temp))
        max_humidity = max(clean_data, key=lambda x: int(x.max_humidity))

        return highest_temp, lowest_temp, max_humidity

    def calculate_month_report(self, clean_data):
        max_temps_avg = sum([int(x.max_temp) for x in clean_data]) / len(clean_data)
        min_temps_avg = sum([int(x.min_temp) for x in clean_data]) / len(clean_data)
        max_humidities_avg = sum([int(x.max_humidity) for x in clean_data]) / len(clean_data)

        return max_temps_avg, min_temps_avg, max_humidities_avg


def check_dir_path(string):
    if string != "path/to/files-dir":
        error_message = "given path is invalid"
        raise argparse.ArgumentTypeError(error_message)

    return string


def seprate_year_month(year_month):
    date_object = datetime.strptime(year_month, "%Y/%m")
    return date_object


def main():
    parser = argparse.ArgumentParser(description="Calculating and showing "
                                                 "weather reports fetched from the data files")
    parser.add_argument("path", type=check_dir_path, help="Directory Destinantion")
    parser.add_argument("-e", "--year", type=str, help="Year Parameter")
    parser.add_argument("-a", "--month", type=seprate_year_month, help="Month Parameter")
    parser.add_argument("-c", "--graphsingle", type=seprate_year_month, help="Show single graph")
    parser.add_argument("-m", "--graphmerged", type=seprate_year_month, help="Show merged graph")
    args = parser.parse_args()

    parser = WeatherReportParse()
    cal_results = CalculateWeatherResults()
    show_results = ShowWeatherResults()

    if args.year:
        clean_weather_record = parser.parse_weather_data(args.path, args.year)

        if clean_weather_record:
            highest_temp, lowest_temp, max_humidity = cal_results.calculate_extreme_report(clean_weather_record)
            show_results.show_extreme_result(highest_temp, lowest_temp, max_humidity)

    if args.month:
        clean_weather_record = parser.parse_weather_data(args.path, args.month)

        if clean_weather_record:
            avg_high_temp, avg_low_temp, avg_hum = cal_results.calculate_month_report(clean_weather_record)
            show_results.show_average_result(avg_high_temp, avg_low_temp, avg_hum)

    if args.graphsingle:
        clean_weather_record = parser.parse_weather_data(args.path, args.graphsingle)

        if clean_weather_record:
            show_results.show_seprate_chart(clean_weather_record)

    if args.graphmerged:
        clean_weather_record = parser.parse_weather_data(args.path, args.graphmerged)

        if clean_weather_record:
            show_results.show_merge_chart(clean_weather_record)


if __name__ == "__main__":
    main()

