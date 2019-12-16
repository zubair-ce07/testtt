import csv
from termcolor import colored, cprint
from argparse import ArgumentParser
import sys
import os
import datetime


class My_ArgParser(ArgumentParser):

    def __init__(self):
        super().__init__(description='Task 1 the Weather Man')
        self.my_add_args()

        self.args = self.parse_args(
            ['weatherman.py',
             '/home/waleed/Desktop/final/the-lab/weatherfiles',
             '-c', '2011/03',
             '-a', '2011/3',
             '-e', '2011'])

    def my_add_args(self):
        self.add_argument(
            'file_name',
            help='name of file')
        self.add_argument(
            'path',
            help='Path to Dir')
        self.add_argument(
            '-a',
            action='store',
            type=lambda s: datetime.datetime.strptime(s, '%Y/%m').date(),
        )
        self.add_argument(
            '-c',
            action='store',
            type=lambda s: datetime.datetime.strptime(s, '%Y/%m').date(),
        )
        self.add_argument(
            '-e',
            action='store',
            type=lambda s: datetime.datetime.strptime(s, '%Y').date(),
        )


class Table:

    def __init__(self, headings=None):
        self.rows = []
        self.headings = []
        self.set_headings(headings)

    def add_row(self, row):
        self.rows.append(row)

    def set_headings(self, headings):
        self.headings = headings

    def print_table(self):
        print(self.headings)
        for row in self.rows:
            print(row)


class Parser:
    file_name = ""

    def __init__(self, file_name):
        self.weather_reading = Table()
        self.file_name = file_name
        if(not(self.file_name.endswith(".txt"))):
            self.file_name = self.file_name + ".txt"
        self.set_weather_reading()

    def type_converstion(self, data):
        data_type = ['string', 'int', 'int', 'int', 'int', 'int', 'int',
                     'int', 'int', 'int', 'float', 'float', 'int', 'float',
                     'float', 'float', 'int', 'int', 'int', 'float',
                     'int', 'string', 'int']

        type_map = {'string': str, 'int': int, 'float': float}
        results = [type_map[t](d or 0) for t, d in zip(data_type, data)]
        return results

    def set_weather_reading(self):

        with open(self.file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                row = [elem.strip() for elem in row]
                if line_count == 0:
                    self.weather_reading.set_headings(row)
                    line_count += 1
                else:
                    self.weather_reading.add_row(self.type_converstion(row))
                    line_count += 1


class Results:
    def __init__(self):
        self.highest_temperature_monthly = []
        self.lowest_temperature_monthly = []
        self.highest_temperature = 0
        self.lowest_temperature = 0
        self.highest_humidity = 0

        self.average_highest_temperature = 0
        self.average_lowest_temperature = 0
        self.average_humidity = 0

    def display_report_A(self):
        print(f"Highest Average: {self.average_highest_temperature:.1f}C")
        print(f"Lowest Average: {self.average_lowest_temperature:.1f}C")
        print(f"Average Mean Humidity: {self.average_humidity:.1f}%")

    def display_report_C(self):
        for index in range(len(self.highest_temperature_monthly)):
            print(index+1, end='')

            for value in range(0, self.lowest_temperature_monthly[index]):
                cprint('+', 'blue', end='')

            for value in range(0, self.highest_temperature_monthly[index]):
                cprint('+', 'red', end='')

            print(
                self.lowest_temperature_monthly[index], "C-", end='', sep='')
            print(self.highest_temperature_monthly[index], "C", sep='')


class CalculateReadings:

    def __init__(self, file_name):
        self.parser = Parser(file_name)
        self.results = Results()

    def cal_highest_average_monthly(self):
        for row in self.parser.weather_reading.rows:
            self.results.average_highest_temperature += row[1]

        self.results.average_highest_temperature\
            /= len(self.parser.weather_reading.rows)

        return self.results.average_highest_temperature

    def cal_lowest_average_monthly(self):
        for row in self.parser.weather_reading.rows:
            self.results.average_lowest_temperature += row[3]

        self.results.average_lowest_temperature \
            /= len(self.parser.weather_reading.rows)

        return self.results.average_lowest_temperature

    def cal_average_mean_humidity_monthly(self):
        for row in self.parser.weather_reading.rows:
            self.results.average_humidity += row[8]

        self.results.average_humidity \
            /= len(self.parser.weather_reading.rows)

        return self.results.average_humidity

    def cal_report_A(self):
        self.cal_highest_average_monthly()
        self.cal_lowest_average_monthly()
        self.cal_average_mean_humidity_monthly()

    def set_highest_lowest_temperature_monthly(self):
        for index in range(len(self.parser.weather_reading.rows)):
            self.results.highest_temperature_monthly.\
                append(self.parser.weather_reading.rows[index][1])
            self.results.lowest_temperature_monthly.\
                append(self.parser.weather_reading.rows[index][3])

    def cal_report_C(self):
        self.set_highest_lowest_temperature_monthly()

    def set_highest_temperature(self):
        self.results.highest_temperature = max(
            elem[1] for elem in self.parser.weather_reading.rows)
        return self.results.highest_temperature

    def set_lowest_temperature(self):
        self.results.lowest_temperature = min(
            elem[3] for elem in self.parser.weather_reading.rows)
        return self.results.lowest_temperature

    def set_highest_humidity(self):
        self.results.highest_humidity = max(
            elem[7] for elem in self.parser.weather_reading.rows)
        return self.results.highest_humidity

    @staticmethod
    def cal_report_E():
        monthly_data = []
        index = 0
        for file_name in os.listdir(arguments.args.path):

            if (file_name.find(str(arguments.args.e.year)) != -1):
                monthly_data.append(CalculateReadings(
                    arguments.args.path+'/'+file_name))

                monthly_data[index].set_highest_temperature()
                monthly_data[index].set_lowest_temperature()
                monthly_data[index].set_highest_humidity()

                index = index+1

        x = max(monthly_data,
                key=lambda item: item.results.highest_temperature)
        y = min(monthly_data,
                key=lambda item: item.results.lowest_temperature)
        z = max(monthly_data,
                key=lambda item: item.results.highest_humidity)

        print(f"Highest: {x.results.highest_temperature}C")
        print(f"Lowest: {y.results.lowest_temperature}C")
        print(f"Humidity: {z.results.highest_humidity}%")


class DisplayReport:

    def __init__(self, file_name):
        self.file_name = file_name

    def report_A(self):
        obj = CalculateReadings(self.file_name)
        obj.cal_report_A()
        obj.results.display_report_A()

    def report_C(self):
        obj = CalculateReadings(self.file_name)
        obj.cal_report_C()
        obj.results.display_report_C()

    def report_E(self):
        CalculateReadings.cal_report_E()


# --------------------------------Main-----------------------------------


arguments = My_ArgParser()


if(arguments.args.a):
    file_name = arguments.args.path+"/Murree_weather_" + \
        str(arguments.args.a.year)+"_"+arguments.args.a.strftime("%b")
    obj = DisplayReport(file_name)
    obj.report_A()


if(arguments.args.c):
    file_name = arguments.args.path+"/Murree_weather_" + \
        str(arguments.args.c.year)+"_"+arguments.args.c.strftime("%b")
    obj = DisplayReport(file_name)
    obj.report_C()


if(arguments.args.e):
    obj = DisplayReport("")
    obj.report_E()
