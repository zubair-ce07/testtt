
import sys
import os
import re
import calendar
import time
import csv
import argparse
from termcolor import colored, cprint

LABELS = ['-e', '-a', '-c', '-b']

class ExtremeWeatherReport(object):
    def __init__(self):
        self.highest_temp_val = -999
        self.highest_temp_day = 'none'
        self.lowest_temp_val = 999
        self.lowest_temp_day = 'none'
        self.humidity_val = -999
        self.humidity_day = 'none'


class DisplayReports(object):
    def __init__(self):
        pass

    def display_extreme_report(self, myreport):
        print('Highest: ' + str(myreport.highest_temp_val) + 'C on '
            + myreport.highest_temp_day)
        print('Lowest: ' + str(myreport.lowest_temp_val) + 'C on '
            + myreport.lowest_temp_day)
        print('Humid: ' + str(myreport.humidity_val) + '% on '
            + myreport.humidity_day)

    def display_average_report(self, myreport):
        print('Highest Average: ' + str(myreport.avg_highest_temp) + 'C')
        print('Lowest Average: ' + str(myreport.avg_lowest_temp) + 'C')
        print('Average Humidity: ' + str(myreport.avg_humidity) + '%')

    def display_chart(self, myreport):
        print(myreport.month + ' ' + str(myreport.year))
        days = len(myreport.highest_temp)
        num = 0
        while num < days:
            max_temp_val = myreport.highest_temp[num]
            plus_str_max_temp = get_plus_str(max_temp_val)
            min_temp_val = myreport.lowest_temp[num]
            plus_str_min_temp = get_plus_str(min_temp_val)
            max_temp_red_str = colored(plus_str_max_temp, 'red')
            min_temp_blue_str = colored(plus_str_min_temp, 'blue')
            num = num + 1
            date = num
            date, max_temp_val, min_temp_val = change_date_temp_format(date, num, max_temp_val, min_temp_val)
            if plus_str_max_temp == '--':
                x = 'Data not available'
                print(date + ' ' + max_temp_val)
            else:
                print(date + ' ' + max_temp_red_str + ' ' + str(max_temp_val) + 'C')

            if plus_str_min_temp == '--':
                min_temp_val = 'Data not available'
                print(date + ' ' + min_temp_val)
            else:
                print(date + ' ' + min_temp_blue_str + ' ' + str(min_temp_val) + 'C')

    def display_bonus_chart(self, myreport):
        print(myreport.month + ' ' + str(myreport.year))
        days = len(myreport.highest_temp)
        num = 0
        while num < days:
            max_temp_val = myreport.highest_temp[num]
            plus_str_max_temp = get_plus_str(max_temp_val)
            min_temp_val = myreport.lowest_temp[num]
            plus_str_min_temp = get_plus_str(min_temp_val)
            max_temp_red_str = colored(plus_str_max_temp, 'red')
            min_temp_blue_str = colored(plus_str_min_temp, 'blue')
            num = num + 1
            date = num
            date, max_temp_val, min_temp_val = change_date_temp_format(date, num, max_temp_val, min_temp_val)
            max_temp_val = str(max_temp_val) + 'C'
            min_temp_val = str(min_temp_val) + 'C'
            if plus_str_max_temp == '--':
                max_temp_val = 'Data not available'
            if plus_str_min_temp == '--':
                min_temp_val = 'Data not available'
            print(date + ' ' + min_temp_blue_str + max_temp_red_str + ' ' + min_temp_val + ' - ' + max_temp_val)


def get_plus_str(num):
    plus_str  = ''
    if num != 'no data':
        for count in range(0, num):
            plus_str = plus_str + '+'
    else:
        plus_str = '--'
    return plus_str

def change_date_temp_format(date, num, max_temp_val, min_temp_val):
    if date < 10:
        date = '0' + str(num)
    else:
        date = str(date)
    if max_temp_val < 10:
        max_temp_val = '0' + str(max_temp_val)
    if min_temp_val < 10:
        min_temp_val = '0' + str(min_temp_val)
    return date, max_temp_val, min_temp_val



class MakeReports(object):
        def __init__(self):
            pass
        def make_extreme_report(self, files, dir_path):
            myreport = ExtremeWeatherReport()
            count = 0
            for filename in files:
                with open(os.path.join(os.sep, dir_path, filename), 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    month_name = get_month_name(filename)
                    for rows in reader:
                        elements = rows[None]
                        count = count + 1
                        if count >= 2  and len(elements) > 1:
                            date = str(count - 1)
                            maxtemp = elements[1]
                            if maxtemp != '' and int(maxtemp) > myreport.highest_temp_val:
                                myreport.highest_temp_val = int(maxtemp)
                                myreport.highest_temp_day = month_name + ' ' + date
                            mintemp = elements[3]
                            if mintemp != '' and int(mintemp) < myreport.lowest_temp_val:
                                myreport.lowest_temp_val = int(mintemp)
                                myreport.lowest_temp_day = month_name + ' ' + date
                            maxhumid = elements[7]
                            if maxhumid != '' and int(maxhumid) > myreport.humidity_val:
                                myreport.humidity_val = int(maxhumid)
                                myreport.humidity_day = month_name + ' ' + date
                count = 0
            return myreport

        def make_average_report(self, filename, dir_path):
            myreport = AverageWeatherReport()
            count = 0
            with open(os.path.join(os.sep, dir_path, filename), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for rows in reader:
                    elements = rows[None]
                    count = count + 1
                    if count >= 2  and len(elements) > 1:
                        maxtemp = elements[1]
                        if maxtemp != '':
                            myreport.avg_highest_temp.append(int(maxtemp))
                        mintemp = elements[3]
                        if mintemp != '':
                            myreport.avg_lowest_temp.append(int(mintemp))
                        maxhumid = elements[7]
                        if maxhumid != '':
                            myreport.avg_humidity.append(int(maxhumid))
            myreport.avg_highest_temp = compute_average(myreport.avg_highest_temp)
            myreport.avg_lowest_temp = compute_average(myreport.avg_lowest_temp)
            myreport.avg_humidity = compute_average(myreport.avg_humidity)
            return myreport


        def make_chart_report(self, filename, dir_path, year):
            myreport = WeatherChartReport()
            count = 0
            with open(os.path.join(os.sep, dir_path, filename), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                month_name = get_month_name(filename)
                myreport.year = year
                myreport.month = month_name
                for rows in reader:
                    elements = rows[None]
                    count = count + 1
                    if count >= 2  and len(elements) > 1:
                        maxtemp = elements[1]
                        if maxtemp != '':
                            myreport.highest_temp.append(int(maxtemp))
                        else:
                            myreport.highest_temp.append('no data')
                        mintemp = elements[3]
                        if mintemp != '':
                            myreport.lowest_temp.append(int(mintemp))
                        else:
                            myreport.lowest_temp.append('no data')
            return myreport


def extreme_weathers(year, dir_path):
    check_year(year)
    all_files = os.listdir(dir_path)
    required_files = []
    for files in all_files:
        if year in files:
            required_files.append(files)
    report_obj = MakeReports()
    myreport = report_obj.make_extreme_report(required_files, dir_path)
    display_obj = DisplayReports()
    display_obj.display_extreme_report(myreport)


class AverageWeatherReport(object):
    def __init__(self):
        self.avg_highest_temp = []
        self.avg_lowest_temp = []
        self.avg_humidity = []


def compute_average(vals):
    return sum(vals)/len(vals)

def get_month_name(filename):
    splited_file_name = filename.split('_')
    month_name = splited_file_name[3][0:3]
    month_name = calendar.month_name[time.strptime(month_name, '%b')[1]]
    return month_name

def check_year(year):
    match_obj = re.match(r'\d{4}', year, re.M|re.I)
    if match_obj is None:
        print('invalid year')
        exit()

def check_year_month(year, month):
    check_year(year)
    if len(month) > 2:
        print('invalid month format')
        exit()
    if int(month) not in list(range(1, 13)):
        print('invalid month')
        exit()


def average_weathers(year_month, dir_path):
    year, english_month = get_year_and_month(year_month)
    required_files = get_files(dir_path, year, english_month)
    report_obj = MakeReports()
    myreport = report_obj.make_average_report(required_files[0], dir_path)
    display_obj = DisplayReports()
    display_obj.display_average_report(myreport)


class WeatherChartReport(object):
    def __init__(self):
        self.year = 0
        self.month = 'none'
        self.highest_temp = []
        self.lowest_temp = []

def get_files(dir_path, year, english_month):
    all_files = os.listdir(dir_path)
    required_files = []
    for files in all_files:
        if year in files:
            if english_month in files:
                required_files.append(files)

    if not required_files:
        print('Data for this month is not available')
        exit()
    return required_files

def get_year_and_month(year_month):
    year_and_month = year_month.split('/')
    year = year_and_month[0]
    month = year_and_month[1]
    check_year_month(year,month)
    if len(month) == 2 and int(month) < 10:
        month = month[1:]
    english_month = calendar.month_abbr[int(month)]
    return year, english_month


def weather_charts(year_month, dir_path, report_label):
    year, english_month = get_year_and_month(year_month)
    required_files = get_files(dir_path, year, english_month)
    report_obj = MakeReports()
    myreport = report_obj.make_chart_report(required_files[0], dir_path, year)
    display_obj = DisplayReports()
    if report_label == '-c':
        display_obj.display_chart(myreport)
    elif report_label == '-b':
        display_obj.display_bonus_chart(myreport)


def check_dirpath_exists(dir_path):
    if not os.path.exists(dir_path):
        print('Directory path does not exist')
        exit()


def check_report_type(report_label):
    if report_label not in LABELS:
        print('invalid report label')
        exit()


def check_args(list_args):
    if len(list_args) != 4:
        print('invalid number of args')
        exit()


def main():
    myparser = argparse.ArgumentParser()
    myparser.add_argument('report-type')
    myparser.add_argument('year-month')
    myparser.add_argument('dir-path')
    args = myparser.parse_args()
    argsdict = vars(args)
    print argsdict

    #list_args = sys.argv
    #check_args(list_args)

    report_label = argsdict['report_type']
    year_month = argsdict['year_month']
    dir_path = argsdict['dir_path']

    check_report_type(report_label)
    check_dirpath_exists(dir_path)

    if report_label == '-e':
        extreme_weathers(year_month, dir_path)
    elif report_label == '-a':
        average_weathers(year_month, dir_path)
    elif report_label == '-c' or report_label == '-b':
        weather_charts(year_month, dir_path, report_label)


if __name__ == '__main__':
    main()
