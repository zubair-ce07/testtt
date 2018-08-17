"""
This module reads weather files and calculate max, min temprature and build charts
"""

import argparse
import calendar
import csv
import os
import re

from termcolor import colored

class WeatherMan:
    """
    This class reads weather files and calculate max, min temprature, build charts
    and print in front of user
    """

    def __init__(self, path):
        self.path = path
        self.file_names = []
        self.month_files = []
        self.max_temp_monthwise = []
        self.low_temp_monthwise = []
        self.date_monthwise = []
        self.humid = []


    def get_files(self, year, month=None):
        """
        This method gets files of desired year and month
        """
        try:
            for files in os.listdir(self.path):
                if re.match('.*' + year + '.*', files):
                    self.file_names.append(files)
            if month is not None:
                for _month in self.file_names:
                    if re.match('.*' + month + '.*', _month):
                        self.month_files.append(_month)
        except IOError as io_error:
            print(io_error)


    def read_from_files(self):
        """
        This method reads files of desired year and month
        """
        if len(self.month_files) > 0:
            self.file_names.clear()
            self.file_names = self.month_files
        for my_file in self.file_names:
            with open('{path}{file_name}'.format(path=self.path, file_name=my_file), 'r') as read_file:
                line = csv.DictReader(read_file)
                for chunk in line:
                    if not (chunk['Max TemperatureC'] or chunk['Min TemperatureC'] or chunk[
                        'Max Humidity']):
                        continue
                    self.max_temp_monthwise.append(chunk['Max TemperatureC'])
                    self.low_temp_monthwise.append(chunk['Min TemperatureC'])
                    self.humid.append(chunk['Max Humidity'])
                    if chunk['PKT'] is not None:
                        self.date_monthwise.append(chunk['PKT'])
                    else:
                        self.date_monthwise.append(chunk['PKST'])


    def temp_list_conversion(self):
        """
        This method converts string lists into integer lists for mathematical operations
        """
        self.max_temp_monthwise = list(map(int, self.max_temp_monthwise))
        self.low_temp_monthwise = list(map(int, self.low_temp_monthwise))
        self.humid = list(map(int, self.humid))


    def show_average(self):
        """
        This method prints max and min average temperature and humidity
        """
        sum_max_temp = sum(self.max_temp_monthwise)
        sum_low_temp = sum(self.low_temp_monthwise)
        sum_humid = sum(self.humid)
        average_max_temp = int(sum_max_temp / len(self.max_temp_monthwise))
        average_low_temp = int(sum_low_temp / len(self.low_temp_monthwise))
        average_humid = int(sum_humid / len(self.humid))
        print('************************************')
        print('Highest Average: {average_max_temp}C '.format(
            average_max_temp=str(average_max_temp)))
        print('Lowest Average: {average_low_temp}C '.format(
            average_low_temp=str(average_low_temp)))
        print('Average Humidity: {average_humid}% '.format(
            average_humid=str(average_humid)))
        print('************************************')


    def date_conversion(self, index):
        """
        This method converts numaric date into english date
        """
        raw_date = index.split('-')
        complete_date = calendar.month_name[int(raw_date[1])]
        complete_date = '{date} {raw_date}'.format(date=complete_date, raw_date=raw_date[2])
        return complete_date


    def combiner(self, year, month=None):
        """
        This method combines combines three common methods in it   
        """
        self.get_files(year, month)
        self.read_from_files()
        self.temp_list_conversion()
    

    def perform_calculation(self):
        """
        This method calculates max, min temperature and max humidity
        and hence finds their relative indeces
        """
        max_value = max(self.max_temp_monthwise)
        min_value = min(self.low_temp_monthwise)
        max_humid = max(self.humid)
        index = self.max_temp_monthwise.index(max_value)
        min_index = self.low_temp_monthwise.index(min_value)
        humid_index = self.humid.index(max_humid)
        return [index, min_index, humid_index]


    def print_data(self):
        """
        This method prints required output of user
        """
        index_list = self.perform_calculation()
        print('************************************')
        print('Highest: {max_temp}C on {date}'.format(max_temp=str(
            self.max_temp_monthwise[index_list[0]]), date=self.date_conversion(self.date_monthwise[index_list[0]])))
        print('Lowest: {low_temp}C on {date}'.format(low_temp=str(
            self.low_temp_monthwise[index_list[1]]), date=self.date_conversion(
                self.date_monthwise[index_list[1]])))
        print('Humidity: {humid}% on {date}'.format(humid=str(
            self.humid[index_list[2]]), date=self.date_conversion(
                self.date_monthwise[index_list[2]])))
        print('************************************')


    def print_chart(self):
        """
        This method prints bar charts
        """
        for max_temp, min_temp, date in zip(self.max_temp_monthwise,
                                            self.low_temp_monthwise, self.date_monthwise):
            print('{date} {color} {m_temp}C'.format(
                date=date, color=colored('+'*max_temp, 'red'), m_temp=str(max_temp)))
            print('{date} {color} {m_temp}C'.format(
                date=date, color=colored('+'*min_temp, 'blue'), m_temp=str(min_temp)))


    def print_bar_chart(self):
        """
        This method prints horizontal bar charts on the same line
        """
        for max_temp, min_temp, date in zip(self.max_temp_monthwise,
                                            self.low_temp_monthwise,
                                            self.date_monthwise):
            print('{date} {color_blue} {color_red}{min_value}C {max_value}C'.format(
                date=date, color_blue=colored('+'*min_temp, 'blue'), color_red=colored(
                    '+'*max_temp, 'red'), min_value=str(min_temp), max_value=str(max_temp)))


def main():
    """
    This method is entry point of program
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-dir', '--path', type=str)
        parser.add_argument('-e', '--year', type=str)
        parser.add_argument('-m', '--month', type=str)
        parser.add_argument('-c', '--monthly_chart', type=str)
        parser.add_argument('-ce', '--monthly_chart_horizontal', type=str)
        args = parser.parse_args()

        weather_man = WeatherMan(args.path)
        if not (args.year or args.month or args.monthly_chart or
                args.monthly_chart_horizontal):
            print("Please enter valid argument")
        elif args.year:
            weather_man.combiner(args.year)
            weather_man.print_data()
        elif args.month:
            weather_man.combiner(args.year, args.month)
            weather_man.show_average()
        elif args.monthly_chart:
            weather_man.combiner(args.year, args.month)
            weather_man.print_chart()
        elif args.monthly_chart_horizontal:
            weather_man.combiner(args.year, args.month)
            weather_man.print_bar_chart()
    except ValueError as value_error:
        print(value_error)

# execution point of program
if __name__ == '__main__':
    main()

