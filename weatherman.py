import csv
import os
import calendar
import argparse
from termcolor import colored


class MonthlyRecord:
    def __init__(self):
        self.max_temp = float("-inf")
        self.min_temp = float("inf")
        self.max_humid = float("-inf")
        self.avg_max_temp = 0
        self.avg_min_temp = 0
        self.avg_mean_humid = 0
        self.max_temp_date = ''
        self.min_temp_date = ''
        self.max_humid_date = ''

    def read_record(self, file_dir):
        sum_max_temp = 0
        sum_min_temp = 0
        sum_mean_humid = 0
        len_max_temp = 0
        len_min_temp = 0
        len_mean_humid = 0
        with open(file_dir, "r") as csv_file:
            weather_file = csv.DictReader(csv_file)
            for row in weather_file:
                if row["Max TemperatureC"]:
                    if int(row["Max TemperatureC"]) > self.max_temp:
                        self.max_temp = int(row["Max TemperatureC"])
                        self.max_temp_date = row["PKT"] if row["PKT"] else row["PKST"]
                    sum_max_temp += int(row["Max TemperatureC"])
                    len_max_temp += 1
                if row["Min TemperatureC"]:
                    if int(row["Min TemperatureC"]) < self.min_temp:
                        self.min_temp = int(row["Min TemperatureC"])
                        self.min_temp_date = row["PKT"] if row["PKT"] else row["PKST"]
                    sum_min_temp += int(row["Min TemperatureC"])
                    len_min_temp += 1
                if row["Max Humidity"] and int(row["Max Humidity"]) > self.max_humid:
                    self.max_humid = int(row["Max Humidity"])
                    self.max_humid_date = row["PKT"] if row["PKT"] else row["PKST"]
                if row[" Mean Humidity"]:
                    sum_mean_humid += int(row[" Mean Humidity"])
                    len_mean_humid += 1

        self.avg_max_temp = round(sum_max_temp / len_max_temp)
        self.avg_min_temp = round(sum_min_temp / len_min_temp)
        self.avg_mean_humid = round(sum_mean_humid / len_mean_humid)

    def calculate_month_weather_results(
            self, input_directory,
            input_year_month):
        year = input_year_month.split('/')[0]
        month = input_year_month.split('/')[1]
        short_month_name = calendar.month_name[int(month)][:3]
        file_name = "Murree_weather_" + year + "_" + short_month_name + ".txt"
        file_path = os.path.join(input_directory, file_name)
        self.read_record(file_path)
        self.print_year_month_results()

    def print_year_month_results(self):
        print("Highest Average:", str(self.avg_max_temp) + 'C')
        print("Lowest Average:", str(self.avg_min_temp) + 'C')
        print("Average Mean Humidity:", str(self.avg_mean_humid) + '%')


class YearRecord:
    def __init__(self):
        self.max_temp_year = float('-inf')
        self.min_temp_year = float('inf')
        self.max_humid_year = float('-inf')
        self.max_temp_date = ''
        self.min_temp_date = ''
        self.max_humid_date = ''

    def calculate_annual_weather_results(self, input_directory, input_year):
        self.read_records(input_directory, input_year)
        self.print_annual_results()

    def read_records(self, input_directory, input_year):
        files = os.listdir(input_directory)
        for file in files:
            if input_year not in file:
                continue
            file_path = os.path.join(input_directory, file)
            month = MonthlyRecord()
            month.read_record(file_path)
            if month.max_temp > self.max_temp_year:
                self.max_temp_year = month.max_temp
                self.max_temp_date = month.max_temp_date
            if month.min_temp < self.min_temp_year:
                self.min_temp_year = month.min_temp
                self.min_temp_date = month.min_temp_date
            if month.max_humid > self.max_humid_year:
                self.max_humid_year = month.max_humid
                self.max_humid_date = month.max_humid_date

    def print_annual_results(self):
        month = self.max_temp_date.split('-')[1]
        day = self.max_temp_date.split('-')[2]
        print('Highest:', str(self.max_temp_year) + 'C', 'on', calendar.month_name[int(month)], day)

        month = self.min_temp_date.split('-')[1]
        day = self.min_temp_date.split('-')[2]
        print('Lowest:', str(self.min_temp_year) + 'C', 'on', calendar.month_name[int(month)], day)

        month = self.max_humid_date.split('-')[1]
        day = self.max_humid_date.split('-')[2]
        print('Humidity:', str(self.max_humid_year) + '%', 'on', calendar.month_name[int(month)], day)


class WeatherGraphs:
    graph_point = '+'

    def display_therm_graph(self, input_directory, input_year_month):
        file_path = self.get_file_path(input_directory, input_year_month)
        self.print_year_month(input_year_month)
        with open(file_path, "r") as csv_file:
            weather_file = csv.DictReader(csv_file)
            for row in weather_file:
                if row["Max TemperatureC"]:
                    max_temp_day = int(row["Max TemperatureC"])
                    high_temp_bar = self.graph_point * max_temp_day
                    day = row["PKT"].split('-')[2]
                    max_temp = row["Max TemperatureC"] + 'C'
                    if int(row["Max TemperatureC"]) < 10:
                        max_temp = '0' + max_temp
                    if int(day) < 10:
                        day = '0' + day
                    print(colored(day, 'cyan'), colored(high_temp_bar, 'red'), colored(max_temp, 'cyan'))
                if row["Min TemperatureC"]:
                    min_temp_day = int(row["Min TemperatureC"])
                    low_temp_bar = self.graph_point * min_temp_day
                    day = row["PKT"].split('-')[2]
                    min_temp = row["Min TemperatureC"] + 'C'
                    if int(row["Min TemperatureC"]) < 10:
                        min_temp = '0' + min_temp
                    if int(day) < 10:
                        day = '0' + day
                    print(colored(day, 'cyan'), colored(low_temp_bar, 'blue'), colored(min_temp, 'cyan'))

    def display_therm_graph_bonus(self, input_directory, input_year_month):
        file_path = self.get_file_path(input_directory, input_year_month)
        self.print_year_month(input_year_month)
        with open(file_path, "r") as csv_file:
            weather_file = csv.DictReader(csv_file)
            for row in weather_file:
                main_temp_bar = ''
                day = ''
                temp_range = ''
                if row["Min TemperatureC"]:
                    min_temp_day = int(row["Min TemperatureC"])
                    low_temp_bar = self.graph_point * min_temp_day
                    main_temp_bar += colored(low_temp_bar, 'blue')
                    day = row["PKT"].split('-')[2]
                    if int(day) < 10:
                        day = '0' + day
                    day = colored(day, 'cyan')
                    min_temp_range = row["Min TemperatureC"] + 'C'
                    if int(row["Min TemperatureC"]) < 10:
                        min_temp_range = '0' + min_temp_range
                    temp_range += min_temp_range + '-'

                if row["Max TemperatureC"]:
                    max_temp_day = int(row["Max TemperatureC"])
                    high_temp_bar = self.graph_point * max_temp_day
                    main_temp_bar += colored(high_temp_bar, 'red')
                    max_temp_range = row["Max TemperatureC"] + 'C'
                    if int(row["Max TemperatureC"]) < 10:
                        max_temp_range = '0' + max_temp_range
                    temp_range += max_temp_range
                    temp_range = colored(temp_range, 'cyan')
                print(day, main_temp_bar, temp_range)

    def get_file_path(self, input_directory, input_year_month):
        year = input_year_month.split('/')[0]
        month = input_year_month.split('/')[1]
        short_month_name = calendar.month_name[int(month)][:3]
        file_name = "Murree_weather_" + year + "_" + short_month_name + ".txt"
        file_path = os.path.join(input_directory, file_name)
        print(calendar.month_name[int(month)], year)
        return file_path

    def print_year_month(self, input_year_month):
        year = input_year_month.split('/')[0]
        month = input_year_month.split('/')[1]
        print(calendar.month_name[int(month)], year)


def main():
    year = YearRecord()
    month = MonthlyRecord()
    graphs = WeatherGraphs()
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str, help="files directory")
    parser.add_argument("-e", "--year", type=str, help="year required")
    parser.add_argument("-a", "--year_month", type=str, help="year/month")
    parser.add_argument("-c", "--year_month_graph", type=str, help="year/month")
    parser.add_argument("-b", "--year_month_graph_bonus", type=str, help="year/month")
    args = parser.parse_args()

    if args.year:
        year.calculate_annual_weather_results(args.directory, args.year)
    if args.year_month:
        month.calculate_month_weather_results(args.directory, args.year_month)
    if args.year_month_graph:
        graphs.display_therm_graph(args.directory, args.year_month_graph)
    if args.year_month_graph_bonus:
        graphs.display_therm_graph_bonus(args.directory, args.year_month_graph_bonus)


if __name__ == '__main__':
    main()

