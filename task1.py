import argparse
import calendar
import csv
import glob
import os
import datetime
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

    def get_year_file_names(self, path, date_time_parse):
        files_names = glob.glob("{}/Murree_weather_{}_*.txt".format(path, date_time_parse.strftime("%Y")))
        return [x.split("/")[3] for x in files_names]

    def read_year_files_record(self, weather_file_names, path):
        weather_report = {}
        for weather_file in weather_file_names:
            month = self.month_to_number[weather_file.split("_")[-1].split(".")[0]]
            file_date = csv.DictReader(open(os.path.join(path, weather_file)))

            valid_data = []
            for x in file_date:
                if x['Max TemperatureC']:
                    valid_data.append(x)

            weather_report.update({month: valid_data})
        return weather_report

    def get_month_file_names(self, path, date_time_parse):

        file_names = glob.glob("{}/Murree_weather_{}_{}.txt".format(path, date_time_parse.strftime("%Y"),
                                                                    date_time_parse.strftime("%b")))
        return [x.split("/")[3] for x in file_names]

    def read_month_files_record(self, weather_file_names, path):
        weather_report = {}
        for weather_file in weather_file_names:
            month = self.month_to_number[weather_file.split("_")[-1].split(".")[0]]
            file_date = csv.DictReader(open(os.path.join(path, weather_file)))

            valid_data = []
            for x in file_date:
                if x['Max TemperatureC']:
                    valid_data.append(x)

            weather_report.update({month: valid_data})

        return weather_report

    def parse_year_data(self, path, date_time_parse):
        weather_file_names = self.get_year_file_names(path, date_time_parse)
        return self.read_year_files_record(weather_file_names, path)

    def parse_month_data(self, path, date_time_parse):

        weather_file_names = self.get_month_file_names(path, date_time_parse)
        return self.read_month_files_record(weather_file_names, path)


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
        max_temps = [int(x.max_temp) for x in clean_data]
        min_temps = [int(x.min_temp) for x in clean_data]
        max_humidities = [int(x.max_humidity) for x in clean_data]

        return sum(max_temps) / len(max_temps), sum(min_temps) / len(min_temps), sum(max_humidities) / len(
            max_humidities)

    def show_extreme_result(self, highest_temp, lowest_temp, max_humidity):
        month_name = calendar.month_name[int(highest_temp.date.split("-")[1])]
        temp = highest_temp.date.split("-")[2]
        print("Highest: {} C on {} {}".format(highest_temp.max_temp, month_name, temp))

        month_name = calendar.month_name[int(lowest_temp.date.split("-")[1])]
        temp = lowest_temp.date.split("-")[2]
        print("Lowest: {} C on {} {}".format(lowest_temp.min_temp, month_name, temp))

        month_name = calendar.month_name[int(max_humidity.date.split("-")[1])]
        temp = max_humidity.date.split("-")[2]
        print("Humidity: {} C on {} {}".format(max_humidity.max_humidity,
                                               month_name, temp))

    def show_average_result(self, avg_high_temp, avg_low_temp, avg_hum):
        print("Highest Average: {} C".format(avg_high_temp))
        print("Lowest Average: {} C".format(avg_low_temp))
        print("Humidity Average: {} per".format(avg_hum))


class DataReport:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(DataReport, self).__new__(self)

        return self._instance

    def show_seprate_chart(self, clean_data):
        for weather_date in clean_data:
            print(weather_date.date.split("-")[-1], end="")

            for i in range(0, int(weather_date.max_temp)):
                print("\033[1;31;40m + ", end="")

            print("{} C".format(weather_date.max_temp))
            print(weather_date.date.split("-")[-1], end="")

            for j in range(0, int(weather_date.min_temp)):
                print("\033[1;34;40m - ", end="")
            print("{} C".format(weather_date.min_temp))

    def show_merge_chart(self, weather_report):
        for weather_date in weather_report:
            print("\033[1;31;40m {}".format(weather_date.date.split("-")[-1]), end="\t")
            print("\033[1;31;40m {} C".format(weather_date.max_temp), end="")

            for i in range(0, int(weather_date.max_temp)):
                print("\033[1;31;40m + ", end="")

            for j in range(0, int(weather_date.min_temp)):
                print("\033[1;34;40m + ", end="")

            print("\033[1;34;40m {} C".format(weather_date.min_temp))


def fetch_clean_data(weather_report):
    clean_data = []
    for weather_month in weather_report:
        for weather_date in weather_report[weather_month]:
            if weather_date["Max TemperatureC"]:
                clean_data.append(CleanWeatherRecord(weather_date["PKT"],
                                                     weather_date["Max TemperatureC"],
                                                     weather_date["Min TemperatureC"],
                                                     weather_date["Max Humidity"]))

    return clean_data


def check_data_validation(weather_report_dic, args_year):
    if not weather_report_dic:
        print("{} is not in the record".format(args_year))
        return 0
    return 1


def check_dir_path(string):
    if string != "path/to/files-dir":
        error_message = "given path is invalid"
        raise argparse.ArgumentTypeError(error_message)

    return string


def main():
    if __name__ == "__main__":
        main()


parser = argparse.ArgumentParser(description="Calculating and showing "
                                             "weather reports fetched from the data files")
parser.add_argument("path", type=check_dir_path, help="Directory Destinantion")
parser.add_argument("-e", "--year", type=int, help="Year Parameter")
parser.add_argument("-a", "--month", type=str, help="Month Parameter")
parser.add_argument("-c", "--graphsingle", type=str, help="Show single graph")
parser.add_argument("-m", "--graphmerged", type=str, help="Show merged graph")
args = parser.parse_args()

parser = WeatherReportParse()
results = DataResults()

if args.year:

    date_time_parse = datetime.datetime(int(args.year), 1, 1)
    weather_report_data = parser.parse_year_data(args.path, date_time_parse)

    if check_data_validation(weather_report_data, args.year):
        clean_weather_data = fetch_clean_data(weather_report_data)
        highest_temp, lowest_temp, max_humidity = results.year_report(clean_weather_data)
        results.show_extreme_result(highest_temp, lowest_temp, max_humidity)

if args.month:
    date_time_parse = datetime.datetime(int(args.month.split("/")[0]), int(args.month.split("/")[1]), 1)
    weather_report_data = parser.parse_month_data(args.path, date_time_parse)

    if check_data_validation(weather_report_data, args.year):
        clean_weather_data = fetch_clean_data(weather_report_data)
        avg_high_temp, avg_low_temp, avg_hum = results.month_report(clean_weather_data)
        results.show_average_result(avg_high_temp, avg_low_temp, avg_hum)

if args.graphsingle:
    date_time_parse = datetime.datetime(int(args.month.split("/")[0]), int(args.month.split("/")[1]), 1)
    weather_report_data = parser.parse_month_data(args.path, date_time_parse)

    if check_data_validation(weather_report_data, args.year):
        clean_weather_data = fetch_clean_data(weather_report_data)
        report = DataReport()
        report.show_seprate_chart(clean_weather_data)

if args.graphmerged:
    date_time_parse = datetime.datetime(int(args.month.split("/")[0]), int(args.month.split("/")[1]), 1)
    weather_report_data = parser.parse_month_data(args.path, date_time_parse)

    if check_data_validation(weather_report_data, args.year):
        clean_weather_data = fetch_clean_data(weather_report_data)
        report = DataReport()
        report.show_merge_chart(clean_weather_data)

