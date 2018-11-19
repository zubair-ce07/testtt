import os.path
import re
import argparse
import datetime
from datetime import date, datetime
from termcolor import colored, cprint


class Weather:
    
    # class variables
    temp_max = []
    temp_low = []
    date_month = []
    max_humidity = []
    mean_humidity = []
    files = []
    files_month = []

    def __init__(self, path):
        self.path = path

    # read data from file and append to lists
    def read_data(self):
        for file in self.files:
            if file != "":
                read_file = (open(self.path+file, "r"))
            for line in read_file:
                line_data = line.split(",")
                date_str = line_data[0]
                date_list = date_str.split('-')
                if date_list[0] not in ("PKT", "PKST"):
                    date_mon = date(year=int(date_list[0]), month=int(date_list[1]),
                                    day=int(date_list[2]))
                    self.date_month.append(date_mon)
                    self.temp_max.append(line_data[1])
                    self.temp_low.append(line_data[2])
                    self.max_humidity.append(line_data[8])
                    self.mean_humidity.append(line_data[9])

    # read a specific year file and store them in files list
    def read_data_year(self, year):
        for f in os.listdir(self.path):
            if re.match('.*'+year+'.*', f):
                self.files.append(f)

    # read specific month file from files list and store it in files_month list
    def read_data_file_month(self, year, month):
        for f in os.listdir(self.path):
            if re.match('.*'+year+'.*', f):
                self.files.append(f)
        for m in self.files:
            if re.match('.*'+month+'.*', m):
                self.files_month.append(m)

    # read a month specific months file records and append to list
    def read_month_data(self):
        for file in self.files_month:
            if file != "":
                read_file = (open(self.path+file, "r"))
            for line in read_file:
                line_data = line.split(",")
                date_str = line_data[0]
                date_list = date_str.split('-')
                if date_list[0] not in ("PKT", "PKST"):
                    date_mon = date(year=int(date_list[0]),
                                    month=int(date_list[1]), day=int(date_list[2]))
                    self.date_month.append(date_mon)
                    self.temp_max.append(line_data[1])
                    self.temp_low.append(line_data[2])
                    self.max_humidity.append(line_data[8])
                    self.mean_humidity.append(line_data[9])

    # removing empty data and converting to integer
    def filter_data(self):
            self.temp_max = filter(None, self.temp_max)
            self.temp_max = list(map(int, self.temp_max))
            self.temp_low = filter(None, self.temp_low)
            self.temp_low = list(map(int, self.temp_low))
            self.max_humidity = filter(None, self.max_humidity)
            self.max_humidity = list(map(int, self.max_humidity))
            self.mean_humidity = filter(None, self.mean_humidity)
            self.mean_humidity = list(map(int, self.mean_humidity))

    # calculate the coldest , hostest and most humid day of year
    def hot_cold_humid_day(self):
        max_temperature = max(self.temp_max)
        min_temperature = min(self.temp_low)
        max_humid = max(self.max_humidity)
        date_strings = [d.strftime(' %B %d') for d in self.date_month]
        h = self.temp_max.index(max_temperature)
        l = self.temp_low.index(min_temperature)
        k = self.max_humidity.index(max_humid)
        print("Highest: " + str(self.temp_max[h]) + "C on " + date_strings[h])
        print("Lowest: " + str(self.temp_low[l]) + "C on " + date_strings[l])
        print("Humidity: " + str(self.max_humidity[k]) + "% on " + date_strings[k])
        print('\n')

    # calculate the average max, average min and average humidity
    def average_max_min_humid_day(self):
        sum_temp = sum(self.temp_max)
        len_temp = len(self.temp_max)
        avg_temp = sum_temp/len_temp

        sum_l_temp = sum(self.temp_low)
        len_l_temp = len(self.temp_low)
        avg_l_temp = sum_l_temp/len_l_temp

        sum_humidity = sum(self.mean_humidity)
        len_humidity = len(self.mean_humidity)
        avg_mean_hum = sum_humidity/len_humidity

        print("Highest Average: " + str(avg_temp) + "C")
        print("Lowest Average: " + str(avg_l_temp) + "C")
        print("Humidity: " + str(avg_mean_hum) + "%")
        print('\n')

    # print two bar graphs
    def max_min_bar(self, month, year):
        s = datetime.strptime(month, '%b')
        m = s.strftime('%B')
        print(m, year)

        hig_max_temp = max(self.temp_max)
        hig_low_temp = min(self.temp_max)
        for i in range(hig_max_temp):
                i = cprint('+', 'red', end=' ')
        print(str(hig_max_temp) + 'C')
        for j in range(hig_low_temp):
            j = cprint('+', 'blue', end=' ')
        print(str(hig_low_temp) + 'C')

        low_max_temp = max(self.temp_low)
        low_min_temp = min(self.temp_low)
        for i in range(low_max_temp):
            i = cprint('+', 'red', end=' ')
        print(str(low_max_temp) + 'C')
        for j in range(low_min_temp):
            j = cprint('+', 'blue', end=' ')
        print(str(low_min_temp) + 'C')

    # print one bar graph
    def one_bar(self, month, year):
        s = datetime.strptime(month, '%b')
        m = s.strftime('%B')
        print(m, year)
        hig_max_temp = max(self.temp_max)
        hig_low_temp = min(self.temp_max)
        for i in range(hig_max_temp):
            i = cprint('+', 'red', end=' ')
        for j in range(hig_low_temp):
            j = cprint('+', 'blue', end=' ')
        print(str(hig_max_temp) + 'C' + '-' + str(hig_low_temp) + 'C')

        low_max_temp = max(self.temp_low)
        low_min_temp = min(self.temp_low)
        for i in range(low_max_temp):
            i = cprint('+', 'red', end=' ')
        for j in range(low_min_temp):
            j = cprint('+', 'blue', end=' ')
        print(str(low_max_temp) + 'C' + '-' + str(low_min_temp) + 'C')
