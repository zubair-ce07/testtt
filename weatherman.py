import argparse
import csv
import datetime
import glob
import json
import os
from collections import defaultdict


class DataReader:
    all_data = defaultdict()

    def __init__(self, file_path):
        self.file_path = file_path

    def loading_data(self):
        for item in os.listdir(self.file_path):
            for weather_file in glob.glob('Murree_weather_*.txt'):
                with open(weather_file) as csvfile:
                    csvReader = csv.DictReader(csvfile)
                    for row in csvReader:
                        self.all_data[row[csvReader.fieldnames[0]]] = row

            return self.all_data


class ResultCalculator:

    def yearly_data_calculation(self, all_data, year):

        self.all_data = all_data
        self.year = year
        max_temp = -1000
        min_temp = 1000
        max_humidity = 0
        max_temp_key = 0
        min_temp_key = 0
        max_humidity_key = 0
        filtered_data = defaultdict()

        for yearly_key in all_data.keys():
            if str(year) in yearly_key:
                filtered_data[yearly_key] = all_data.get(yearly_key)

        for filtered_key, filtered_value in filtered_data.items():
            for key, value in list(filtered_value.items()):
                if key == 'Max TemperatureC' and value:
                    if int(filtered_value[key]) > int(max_temp):
                        max_temp = filtered_value[key]
                        max_temp_key = filtered_key

                if key == 'Max Humidity' and value:
                    if int(filtered_value[key]) > int(max_humidity):
                        max_humidity = filtered_value[key]
                        max_humidity_key = filtered_key

                if key == 'Min TemperatureC' and value:
                    if int(filtered_value[key]) < int(min_temp):
                        min_temp = filtered_value[key]
                        min_temp_key = filtered_key

        print('Maximum temperature value {} was recorded on {}'.format(max_temp, max_temp_key))
        print('Minimum temperature value {} was recorded on {}'.format(min_temp, min_temp_key))
        print('Maximum humidity value {} was recorded on {} '.format(max_humidity, max_humidity_key))

    def monthly_data_calculation(self, all_data, year, month):

        self.all_data = all_data
        self.year = year

        self.month = month
        sum_highest_temp = 0
        sum_lowest_temp = 0
        sum_mean_humidity = 0
        filtered_data = defaultdict()

        for monthly_key in all_data.keys():
            if '{}-{}'.format(year, month) in monthly_key:
                filtered_data[monthly_key] = all_data.get(monthly_key)

        for filtered_key, filtered_value in filtered_data.items():

            for key, value in list(filtered_value.items()):
                if key == 'Max TemperatureC' and value:
                    sum_highest_temp = sum_highest_temp + int(filtered_value[key])
                if key == 'Min TemperatureC' and value:
                    sum_lowest_temp = sum_lowest_temp + int(filtered_value[key])
                if key == ' Mean Humidity' and value:
                    sum_mean_humidity = sum_mean_humidity + int(filtered_value[key])

        print('Average Highest Temperature was {} C'.format(sum_highest_temp / len(list(filtered_data.keys()))))
        print('Average Lowest Temperature was {} C'.format(sum_lowest_temp / len(list(filtered_data.keys()))))
        print('Average Mean Humidity was {} C'.format(sum_mean_humidity / len(list(filtered_data.keys()))))

    def monthly_graph_plotting(self, all_data, year, month):

        self.all_data = all_data
        self.year = year
        self.month = month
        list_max_temp = []
        list_min_temp = []
        filtered_data = defaultdict()
        graph_loop_var = 0
        multi_graph_var = 0
        red = '\033[91m'
        blue = '\033[94m'

        for all_keys, all_values in all_data.items():
            for key, value in list(all_values.items()):
                if not value:
                    all_values[key] = str(0)

        for k in all_data.keys():
            if '{}-{}'.format(year, month) in k:
                filtered_data[k] = all_data.get(k)

        for filtered_key, filtered_value in filtered_data.items():
            for key, value in filtered_value.items():
                if key == 'Max TemperatureC':
                    list_max_temp.append(int(filtered_value[key]))
                if key == 'Min TemperatureC':
                    list_min_temp.append(int(filtered_value[key]))

        while graph_loop_var < len(list_max_temp):
            print(graph_loop_var, red, '+' * list_max_temp[graph_loop_var], list_max_temp[graph_loop_var], 'C')
            print(graph_loop_var, blue, '+' * list_min_temp[graph_loop_var], list_min_temp[graph_loop_var], 'C')
            graph_loop_var += 1

        while multi_graph_var < len(list_max_temp):
            print(
                multi_graph_var, blue, '+' * list_min_temp[multi_graph_var], red, '+' * list_max_temp[multi_graph_var],
                list_min_temp[multi_graph_var], 'C', '-',
                list_max_temp[multi_graph_var],
                'C')
            multi_graph_var += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Enter the path to directory containing your weather files')
    parser.add_argument('-e', '--date_year', type=str)
    parser.add_argument('-a', '--date_month', type=str)
    parser.add_argument('-c', '--date_multi_reports', type=str)

    args = parser.parse_args()
    file_path = args.path
    load_data = DataReader(file_path)
    all_data = load_data.loading_data()
    calculate_result = ResultCalculator()

    if args.date_month:
        date_month = args.date_month
        date_month = datetime.datetime.strptime(date_month, "%Y/%m")
        calculate_result.monthly_data_calculation(all_data, date_month.year, date_month.month)

    if args.date_multi_reports:
        date_multi_reports = args.date_multi_reports
        date_multi_reports = datetime.datetime.strptime(date_multi_reports, "%Y/%m")
        calculate_result.monthly_graph_plotting(all_data, date_multi_reports.year, date_multi_reports.month)

    if args.date_year:
        date_year = args.date_year
        calculate_result.yearly_data_calculation(all_data, date_year)


if __name__ == '__main__':
    main()
