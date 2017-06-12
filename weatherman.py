import csv
import os
import calendar
import argparse
from termcolor import colored


class Month:
    def __init__(self):
        self.max_temp = 0
        self.min_temp = 0
        self.max_humid = 0
        self.avg_max_temp = 0
        self.avg_min_temp = 0
        self.avg_mean_humid = 0
        self.max_temp_date = ''
        self.min_temp_date = ''
        self.max_humid_date = ''

    def read_data_from_file(self, file_dir):
        max_temp_days = {}
        min_temp_days = {}
        max_humid_days = {}
        mean_humid_days = []
        with open(file_dir, "rU") as csv_file:
            weather_file = csv.DictReader(csv_file)
            for row in weather_file:
                if row["Max TemperatureC"]:
                    max_temp_days[row["PKT"]] = int(row["Max TemperatureC"])
                if row["Min TemperatureC"]:
                    min_temp_days[row["PKT"]] = int(row["Min TemperatureC"])
                if row["Max Humidity"]:
                    max_humid_days[row["PKT"]] = int(row["Max Humidity"])
                if row[" Mean Humidity"]:
                    mean_humid_days.append(int(row[" Mean Humidity"]))
        self.max_temp_date = max(max_temp_days, key=max_temp_days.get)
        self.max_temp = max_temp_days[self.max_temp_date]
        self.min_temp_date = min(min_temp_days, key=min_temp_days.get)
        self.min_temp = min_temp_days[self.min_temp_date]
        self.max_humid_date = max(max_humid_days, key=max_humid_days.get)
        self.max_humid = max_humid_days[self.max_humid_date]
        self.avg_max_temp = round(sum(max_temp_days.values()) / (len(max_temp_days)))
        self.avg_min_temp = round(sum(min_temp_days.values()) / (len(min_temp_days)))
        self.avg_mean_humid = round(sum(mean_humid_days) / (len(mean_humid_days)))

    def calculate_year_month_weather_results(
            self, input_directory,
            input_year_month):
        year = input_year_month.split('/')[0]
        month = input_year_month.split('/')[1]
        short_month_name = calendar.month_name[int(month)][:3]
        file_name = "Murree_weather_" + year + "_" + short_month_name + ".txt"
        file_path = os.path.join(input_directory, file_name)
        self.read_data_from_file(file_path)
        self.print_year_month_results()

    def print_year_month_results(self):
        print("Highest Average:", str(self.avg_max_temp) + 'C')
        print("Lowest Average:", str(self.avg_min_temp) + 'C')
        print("Average Mean Humidity:", str(self.avg_mean_humid) + '%')


class Year:
    def calculate_annual_weather_results(self, input_directory, input_year):
        max_temp_months = {}
        min_temp_months = {}
        max_humid_months = {}
        month = Month()
        files = os.listdir(input_directory)
        for file in files:
            if input_year not in file:
                continue
            file_path = os.path.join(input_directory, file)
            month.read_data_from_file(file_path)
            max_temp_months[month.max_temp_date] = month.max_temp
            min_temp_months[month.min_temp_date] = month.min_temp
            max_humid_months[month.max_humid_date] = month.max_humid

        max_temp_date = max(max_temp_months, key=max_temp_months.get)
        max_temp = max_temp_months[max_temp_date]
        min_temp_date = min(min_temp_months, key=min_temp_months.get)
        min_temp = min_temp_months[min_temp_date]
        max_humid_date = max(max_humid_months, key=max_humid_months.get)
        max_humid = max_humid_months[max_humid_date]
        self.print_annual_results(
            max_temp, min_temp,
            max_humid, max_temp_date,
            min_temp_date, max_humid_date)

    def print_annual_results(
            self, max_temp, min_temp,
            max_humid, max_temp_date,
            min_temp_date, max_humid_date):

        month = max_temp_date.split('-')[1]
        day = max_temp_date.split('-')[2]
        print('Highest:', str(max_temp) + 'C', 'on', calendar.month_name[int(month)], day)

        month = min_temp_date.split('-')[1]
        day = min_temp_date.split('-')[2]
        print('Lowest:', str(min_temp) + 'C', 'on', calendar.month_name[int(month)], day)

        month = max_humid_date.split('-')[1]
        day = max_humid_date.split('-')[2]
        print('Humidity:', str(max_humid) + '%', 'on', calendar.month_name[int(month)], day)


class WeatherGraphs:
    graph_point = '+'

    def display_therm_graph(self, input_directory, input_year_month):
        file_path = self.get_file_path(input_directory, input_year_month)
        self.print_year_month(input_year_month)
        with open(file_path, "rU") as csv_file:
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
        with open(file_path, "rU") as csv_file:
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
    year = Year()
    month = Month()
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
        month.calculate_year_month_weather_results(args.directory, args.year_month)
    if args.year_month_graph:
        graphs.display_therm_graph(args.directory, args.year_month_graph)
    if args.year_month_graph_bonus:
        graphs.display_therm_graph_bonus(args.directory, args.year_month_graph_bonus)


if __name__ == '__main__':
    main()

