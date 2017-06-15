import sys
import os
import re
import calendar
import time
import csv
import argparse
from termcolor import colored, cprint

class ExtremeWeatherReport(object):
    def __init__(self):
        self.highest_temp_val = -999
        self.highest_temp_day = 'none'
        self.lowest_temp_val = 999
        self.lowest_temp_day = 'none'
        self.humidity_val = -999
        self.humidity_day = 'none'


class AverageWeatherReport(object):
    def __init__(self):
        self.avg_highest_temp = []
        self.avg_lowest_temp = []
        self.avg_humidity = []


class WeatherChartReport(object):
    def __init__(self):
        self.year = 0
        self.month = 'none'
        self.highest_temp = []
        self.lowest_temp = []


class MakeReports(object):
        def make_extreme_report(self, files, dir_path):
            myreport = ExtremeWeatherReport()
            set_helper = SetHelper()
            check_helper = CheckHelper()
            for filename in files:
                with open(os.path.join(os.sep, dir_path, filename), 'r') as csvfile:
                    next(csvfile)
                    reader = csv.DictReader(csvfile)
                    for rows in reader:
                        if check_helper.check_endoffile(rows):
                            break
                        myreport = set_helper.set_extreme_vals(myreport, rows)
            return myreport

        def make_average_report(self, filename, dir_path):
            myreport = AverageWeatherReport()
            check_helper = CheckHelper()
            set_helper = SetHelper()
            with open(os.path.join(os.sep, dir_path, filename), 'r') as csvfile:
                next(csvfile)
                reader = csv.DictReader(csvfile)
                for rows in reader:
                    if check_helper.check_endoffile(rows):
                        break
                    myreport = set_helper.set_average_vals(myreport, rows)
            get_helper = GetHelper()
            myreport.avg_highest_temp = get_helper.compute_average(myreport.avg_highest_temp)
            myreport.avg_lowest_temp = get_helper.compute_average(myreport.avg_lowest_temp)
            myreport.avg_humidity = get_helper.compute_average(myreport.avg_humidity)
            return myreport

        def make_chart_report(self, filename, dir_path, year):
            myreport = WeatherChartReport()
            get_helper = GetHelper()
            check_helper = CheckHelper()
            set_helper = SetHelper()
            with open(os.path.join(os.sep, dir_path, filename), 'r') as csvfile:
                next(csvfile)
                reader = csv.DictReader(csvfile)
                myreport.year = year
                myreport.month = get_helper.get_month_name(filename)
                for rows in reader:
                    if check_helper.check_endoffile(rows):
                        break
                    myreport = set_helper.set_chart_report_vals(myreport, rows)
            return myreport


class DisplayReports(object):
    def display_extreme_report(self, myreport):
        print('Highest: {0}C on {1}'.format(str(myreport.highest_temp_val), myreport.highest_temp_day))
        print('Lowest: {0}C on {1}'.format(str(myreport.lowest_temp_val), myreport.lowest_temp_day))
        print('Humid: {0}% on {1}'.format(str(myreport.humidity_val), myreport.humidity_day))

    def display_average_report(self, myreport):
        print('Highest Average: {}C'.format(str(myreport.avg_highest_temp)))
        print('Lowest Average: {}C'.format(str(myreport.avg_lowest_temp)))
        print('Average Humidity: {}%'.format(str(myreport.avg_humidity)))

    def display_chart(self, myreport):
        get_helper = GetHelper()
        get_helper.print_month_year(myreport)
        days = len(myreport.highest_temp)
        num = 0
        while num < days:
            (max_temp_val, min_temp_val,
             plus_str_max_temp, plus_str_min_temp,
             max_temp_red_str, min_temp_blue_str) = get_helper.get_temp_vals_and_str(myreport, num)
            num = num + 1
            date = num
            date, max_temp_val, min_temp_val = get_helper.change_date_temp_format(date, num,
                                                                    max_temp_val,
                                                                    min_temp_val)
            if plus_str_max_temp == '--':
                max_temp_val = 'Data not available'
                print('{0} {1}'.format(date, max_temp_val))
            else:
                print('{0} {1} {2}C'.format(date, max_temp_red_str, str(max_temp_val)))

            if plus_str_min_temp == '--':
                min_temp_val = 'Data not available'
                print('{0} {1}'.format(date, min_temp_val))
            else:
                print('{0} {1} {2}C'.format(date, min_temp_blue_str, str(min_temp_val)))

    def display_bonus_chart(self, myreport):
        get_helper = GetHelper()
        get_helper.print_month_year(myreport)
        days = len(myreport.highest_temp)
        num = 0
        while num < days:
            (max_temp_val, min_temp_val,
             plus_str_max_temp, plus_str_min_temp,
             max_temp_red_str, min_temp_blue_str) = get_helper.get_temp_vals_and_str(myreport, num)
            num = num + 1
            date = num
            date, max_temp_val, min_temp_val = get_helper.change_date_temp_format(date, num,
                                                                    max_temp_val,
                                                                    min_temp_val)
            max_temp_val = '{}C'.format(str(max_temp_val))
            min_temp_val = '{}C'.format(str(min_temp_val))
            if plus_str_max_temp == '--':
                max_temp_val = 'Data not available'
            if plus_str_min_temp == '--':
                min_temp_val = 'Data not available'
            print('{0} {1}{2} {3}-{4}'.format(date, min_temp_blue_str, max_temp_red_str,
                                              min_temp_val, max_temp_val))


class GetHelper():
    def get_temp_vals_and_str(self, myreport, num):
        get_helper = GetHelper()
        max_temp_val = myreport.highest_temp[num]
        plus_str_max_temp = get_helper.get_plus_str(max_temp_val)
        min_temp_val = myreport.lowest_temp[num]
        plus_str_min_temp = get_helper.get_plus_str(min_temp_val)
        max_temp_red_str = colored(plus_str_max_temp, 'red')
        min_temp_blue_str = colored(plus_str_min_temp, 'blue')
        return (max_temp_val, min_temp_val, plus_str_max_temp,
            plus_str_min_temp, max_temp_red_str, min_temp_blue_str)

    def get_plus_str(self, num):
        plus_str  = ''
        if num != 'no data':
            for count in range(0, num):
                plus_str = '{}+'.format(plus_str)
        else:
            plus_str = '--'
        return plus_str

    def get_month_name(self, filename):
        splited_file_name = filename.split('_')
        month_name = splited_file_name[3][0:3]
        month_name = calendar.month_name[time.strptime(month_name, '%b')[1]]
        return month_name

    def get_date(self, date):
        return time.strftime('%B %d',time.strptime(date, '%Y-%m-%d'))

    def get_files(self, dir_path, year, english_month):
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

    def get_year_and_month(self, year_month):
        year_and_month = year_month.split('/')
        year = year_and_month[0]
        month = year_and_month[1]
        check_helper = CheckHelper()
        check_helper.check_year_month(year,month)
        if len(month) == 2 and int(month) < 10:
            month = month[1:]
        english_month = calendar.month_abbr[int(month)]
        return year, english_month

    def change_date_temp_format(self, date, num, max_temp_val, min_temp_val):
        if date < 10:
            date = '0{}'.format(str(num))
        else:
            date = str(date)
        if max_temp_val < 10:
            max_temp_val = '0{}'.format(str(max_temp_val))
        if min_temp_val < 10:
            min_temp_val = '0{}'.format(str(min_temp_val))
        return date, max_temp_val, min_temp_val

    def compute_average(self, vals):
        return sum(vals)/len(vals)

    def print_month_year(self, myreport):
        print('{0} {1}'.format(myreport.month, str(myreport.year)))


class CheckHelper():
    def check_dirpath_exists(self, dir_path):
        if not os.path.exists(dir_path):
            print('Directory path does not exist')
            exit()

    def check_year_month(self, year, month):
        check_helper = CheckHelper()
        check_helper.check_year(year)
        match_obj = re.match(r'\d{1}', month, re.M|re.I)
        if match_obj is None:
            print('invalid month')
            exit()
        if len(month) > 2:
            print('invalid month format')
            exit()
        if int(month) not in list(range(1, 13)):
            print('invalid month')
            exit()

    def check_year(self, year):
        match_obj = re.match(r'\d{4}', year, re.M|re.I)
        if match_obj is None:
            print('invalid year')
            exit()
    def check_endoffile(self, rows):
        if re.findall(r'(?:^<)',rows['PKT']):
            return True
        else:
            return False


class SetHelper():
    def set_extreme_vals(self, myreport, rows):
        get_helper = GetHelper()
        maxtemp = rows['Max TemperatureC']
        if maxtemp != '' and int(maxtemp) > myreport.highest_temp_val:
            myreport.highest_temp_val = int(maxtemp)
            myreport.highest_temp_day = get_helper.get_date(rows['PKT'])
        mintemp = rows['Min TemperatureC']
        if mintemp != '' and int(mintemp) < myreport.lowest_temp_val:
            myreport.lowest_temp_val = int(mintemp)
            myreport.lowest_temp_day = get_helper.get_date(rows['PKT'])
        maxhumid = rows['Max Humidity']
        if maxhumid != '' and int(maxhumid) > myreport.humidity_val:
            myreport.humidity_val = int(maxhumid)
            myreport.humidity_day = get_helper.get_date(rows['PKT'])
        return myreport

    def set_average_vals(self, myreport, rows):
        maxtemp = rows['Max TemperatureC']
        if maxtemp != '':
            myreport.avg_highest_temp.append(int(maxtemp))
        mintemp = rows['Min TemperatureC']
        if mintemp != '':
            myreport.avg_lowest_temp.append(int(mintemp))
        maxhumid = rows['Max Humidity']
        if maxhumid != '':
            myreport.avg_humidity.append(int(maxhumid))
        return myreport

    def set_chart_report_vals(self, myreport, rows):
        maxtemp = rows['Max TemperatureC']
        if maxtemp != '':
            myreport.highest_temp.append(int(maxtemp))
        else:
            myreport.highest_temp.append('no data')
        mintemp = rows['Min TemperatureC']
        if mintemp != '':
            myreport.lowest_temp.append(int(mintemp))
        else:
            myreport.lowest_temp.append('no data')
        return myreport


def extreme_weathers(year, dir_path):
    check_helper = CheckHelper()
    check_helper.check_year(year)
    all_files = os.listdir(dir_path)
    required_files = []
    for files in all_files:
        if year in files:
            required_files.append(files)
    report_obj = MakeReports()
    myreport = report_obj.make_extreme_report(required_files, dir_path)
    display_obj = DisplayReports()
    display_obj.display_extreme_report(myreport)


def average_weathers(year_month, dir_path):
    get_helper = GetHelper()
    year, english_month = get_helper.get_year_and_month(year_month)
    required_files = get_helper.get_files(dir_path, year, english_month)
    report_obj = MakeReports()
    myreport = report_obj.make_average_report(required_files[0], dir_path)
    display_obj = DisplayReports()
    display_obj.display_average_report(myreport)


def weather_charts(year_month, dir_path, report_label):
    get_helper = GetHelper()
    year, english_month = get_helper.get_year_and_month(year_month)
    required_files = get_helper.get_files(dir_path, year, english_month)
    report_obj = MakeReports()
    myreport = report_obj.make_chart_report(required_files[0], dir_path, year)
    display_obj = DisplayReports()
    if report_label == '-c':
        display_obj.display_chart(myreport)
    elif report_label == '-b':
        display_obj.display_bonus_chart(myreport)


def main():
    myparser = argparse.ArgumentParser()
    myparser.add_argument('-e', '--extreme-report',
                        help = 'For generating extreme weather report. Takes year as an input')
    myparser.add_argument('-a', '--average-report',
                        help = 'For generating average weather report. Takes year and month as an input')
    myparser.add_argument('-c', '--doublechart-report',
                        help = 'For generating two horizontal bar chart for each day. Takes year and month as an input')
    myparser.add_argument('-b', '--singlechart-report',
                        help = 'For generating one horizontal bar chart for each day. Takes year as an input')
    myparser.add_argument('dirpath',
                        help = 'Give directory path of weather data')
    args = myparser.parse_args()
    dir_path = args.dirpath
    check_helper = CheckHelper()
    check_helper.check_dirpath_exists(dir_path)
    if args.extreme_report:
        extreme_weathers(args.extreme_report, dir_path)
    elif args.average_report:
        average_weathers(args.average_report, dir_path)
    elif args.doublechart_report:
        report_label = '-c'
        weather_charts(args.doublechart_report, dir_path, report_label)
    elif args.singlechart_report:
        report_label = '-b'
        weather_charts(args.singlechart_report, dir_path, report_label)
    else:
        print('No Report Label Matched')
        exit()


if __name__ == '__main__':
    main()
