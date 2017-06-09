import csv
import os
import fnmatch
import calendar
import argparse
from termcolor import colored


class WeatherRecord:
    highest_temp_month = 0
    lowest_temp_month = 0
    most_humid_month = 0
    avg_max_temp_days = 0
    avg_min_temp_days = 0
    avg_mean_humid_days = 0
    highest_temp_month_date = ""
    lowest_temp_month_date = ""
    most_humid_month_date = ""

    def __init__(self):
        self.highest_temp_month = 0
        self.lowest_temp_month = 0
        self.most_humid_month = 0
        self.highest_temp_month_date = ""
        self.lowest_temp_month_date = ""
        self.most_humid_month_date = ""

    def calculate_annual_weather_results(self, input_directory, input_year):
        input_filter = "*" + input_year + "*.txt"
        max_temp_months = []
        min_temp_months = []
        max_humid_months = []
        max_temp_months_dates = []
        min_temp_months_dates = []
        max_humid_months_dates = []
        files = os.listdir(input_directory)

        for file in fnmatch.filter(files, input_filter):
            file_path = os.path.join(input_directory, file)
            self.calculate_monthly_weather_stats(file_path)
            max_temp_months.append(self.highest_temp_month)
            min_temp_months.append(self.lowest_temp_month)
            max_humid_months.append(self.most_humid_month)
            max_temp_months_dates.append(self.highest_temp_month_date)
            min_temp_months_dates.append(self.lowest_temp_month_date)
            max_humid_months_dates.append(self.most_humid_month_date)

        max_temp_year = max(max_temp_months)
        max_temp_year_date = max_temp_months_dates[max_temp_months.index(max_temp_year)]
        min_temp_year = min(min_temp_months)
        min_temp_year_date = min_temp_months_dates[min_temp_months.index(min_temp_year)]
        max_humid_year = max(max_humid_months)
        max_humid_year_date = max_humid_months_dates[max_humid_months.index(max_humid_year)]

        self.print_annual_results(
            max_temp_year, min_temp_year,
            max_humid_year, max_temp_year_date,
            min_temp_year_date, max_humid_year_date)

    def calculate_monthly_weather_stats(self, file_dir):
        max_temp_days = []
        min_temp_days = []
        max_humid_days = []
        max_temp_days_dates = []
        min_temp_days_dates = []
        max_humid_days_dates = []
        mean_humid_days = []
        with open(file_dir, "rU") as inp:
            rd = csv.DictReader(inp)
            for row in rd:
                if not row["Max TemperatureC"] == '':
                    max_temp_days.append(int(row["Max TemperatureC"]))
                    max_temp_days_dates.append(row["PKT"])
                if not row["Min TemperatureC"] == '':
                    min_temp_days.append(int(row["Min TemperatureC"]))
                    min_temp_days_dates.append(row["PKT"])
                if not row["Max Humidity"] == '':
                    max_humid_days.append(int(row["Max Humidity"]))
                    max_humid_days_dates.append(row["PKT"])
                if not row[" Mean Humidity"] == '':
                    mean_humid_days.append(int(row[" Mean Humidity"]))

        self.highest_temp_month = max(max_temp_days)
        self.lowest_temp_month = min(min_temp_days)
        self.most_humid_month = max(max_humid_days)
        self.highest_temp_month_date = max_temp_days_dates[max_temp_days.index(self.highest_temp_month)]
        self.lowest_temp_month_date = min_temp_days_dates[min_temp_days.index(self.lowest_temp_month)]
        self.most_humid_month_date = max_humid_days_dates[max_humid_days.index(self.most_humid_month)]
        self.avg_max_temp_days = round(sum(max_temp_days) / (len(max_temp_days)))
        self.avg_min_temp_days = round(sum(min_temp_days) / (len(min_temp_days)))
        self.avg_mean_humid_days = round(sum(mean_humid_days) / (len(mean_humid_days)))

    def print_annual_results(
            self, max_temp_year, min_temp_year,
            max_humid_year, max_temp_year_date,
            min_temp_year_date, max_humid_year_date):

        month = max_temp_year_date.split('-')[1]
        day = max_temp_year_date.split('-')[2]
        temp_str = str(max_temp_year) + 'C'
        print('Highest:', temp_str, 'on', calendar.month_name[int(month)], day)

        month = min_temp_year_date.split('-')[1]
        day = min_temp_year_date.split('-')[2]
        temp_str = str(min_temp_year) + 'C'
        print('Lowest:', temp_str, 'on', calendar.month_name[int(month)], day)

        month = max_humid_year_date.split('-')[1]
        day = max_humid_year_date.split('-')[2]
        temp_str = str(max_humid_year) + '%'
        print('Humidity:', temp_str, 'on', calendar.month_name[int(month)], day)

    def calculate_year_month_weather_results(
            self, input_directory,
            input_year_month):
        year = input_year_month.split('/')[0]
        month = input_year_month.split('/')[1]
        short_month_name = calendar.month_name[int(month)][:3]
        file_name = "Murree_weather_" + year + "_" + short_month_name + ".txt"
        file_path = os.path.join(input_directory, file_name)
        self.calculate_monthly_weather_stats(file_path)
        self.print_year_month_results()

    def print_year_month_results(self):
        str_h_temp = str(self.avg_max_temp_days) + 'C'
        str_l_temp = str(self.avg_min_temp_days) + 'C'
        str_humid = str(self.avg_mean_humid_days) + '%'
        print("Highest Average:", str_h_temp)
        print("Lowest Average:", str_l_temp)
        print("Average Mean Humidity:", str_humid)


class WeatherGraphs:
    graph_point = '+'

    def display_therm_graph(self, input_directory, input_year_month):
        file_path = self.get_file_path(input_directory, input_year_month)
        self.print_year_month(input_year_month)
        with open(file_path, "rU") as inp:
            rd = csv.DictReader(inp)
            for row in rd:
                if not row["Max TemperatureC"] == '':
                    max_temp_day = int(row["Max TemperatureC"])
                    high_temp_bar = self.graph_point * max_temp_day
                    day = row["PKT"].split('-')[2]
                    max_temp = row["Max TemperatureC"] + 'C'
                    if int(row["Max TemperatureC"]) < 10:
                        max_temp = '0' + max_temp
                    if int(day) < 10:
                        day = '0' + day
                    print(colored(day, 'cyan'), colored(high_temp_bar, 'red'), colored(max_temp, 'cyan'))
                if not row["Min TemperatureC"] == '':
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
        with open(file_path, "rU") as inp:
            rd = csv.DictReader(inp)
            for row in rd:
                main_temp_bar = ''
                day = ''
                temp_range = ''
                if row["Min TemperatureC"] != '':
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

                if row["Max TemperatureC"] != '':
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
    records = WeatherRecord()
    graphs = WeatherGraphs()
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str, help="files directory")
    parser.add_argument("-e", "--year", type=str, help="year required")
    parser.add_argument("-a", "--year_month", type=str, help="year/month")
    parser.add_argument("-c", "--year_month_graph", type=str, help="year/month")
    parser.add_argument("-b", "--year_month_graph_bonus", type=str, help="year/month")
    args = parser.parse_args()

    if args.year:
        records.calculate_annual_weather_results(args.directory, args.year)
    if args.year_month:
        records.calculate_year_month_weather_results(args.directory, args.year_month)
    if args.year_month_graph:
        graphs.display_therm_graph(args.directory, args.year_month_graph)
    if args.year_month_graph_bonus:
        graphs.display_therm_graph_bonus(args.directory, args.year_month_graph_bonus)


if __name__ == '__main__':
    main()

