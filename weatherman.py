import sys
import os
import re
import calendar
import time
import csv
import argparse
from termcolor import colored


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


class ReportMaker(object):
    def make_extreme_report(self, files, dir_path):
        myreport = ExtremeWeatherReport()
        extract_temp_vals = TemperatureValuesExtractor()
        for filename in files:
            self.read_files(filename, dir_path, '-e', myreport, extract_temp_vals)
        return myreport

    def make_average_report(self, filename, dir_path):
        myreport = AverageWeatherReport()
        extract_temp_vals = TemperatureValuesExtractor()
        self.read_files(filename, dir_path, '-a', myreport, extract_temp_vals)
        myreport.avg_highest_temp = self.compute_average(myreport.avg_highest_temp)
        myreport.avg_lowest_temp = self.compute_average(myreport.avg_lowest_temp)
        myreport.avg_humidity = self.compute_average(myreport.avg_humidity)
        return myreport

    def make_chart_report(self, filename, dir_path, year):
        myreport = WeatherChartReport()
        myreport.year = year
        extract_temp_vals = TemperatureValuesExtractor()
        self.read_files(filename, dir_path, '-c', myreport, extract_temp_vals)
        return myreport

    def read_files(self, filename, dir_path,flag, myreport, extract_temp_vals):
        with open(os.path.join(os.sep, dir_path, filename), 'r') as csvfile:
            next(csvfile)
            reader = csv.DictReader(csvfile)
            for rows in reader:
                if Validator.temperature_values_are_none(rows):
                    break
                if flag == '-e':
                    myreport = extract_temp_vals.extract_extreme_vals(myreport, rows)
                elif flag == '-a':
                    myreport = extract_temp_vals.extract_average_vals(myreport, rows)
                else:
                    myreport = extract_temp_vals.extract_chart_report_vals(myreport, rows)
                    myreport.month = VariableFormatter.fetch_standard_month_name(filename)

    def compute_average(self, vals):
        return sum(vals)/len(vals)


class ReportDisplayer(object):
    def display_extreme_report(self, myreport):
        print('Highest: {0}C on {1}'.format(str(myreport.highest_temp_val), myreport.highest_temp_day))
        print('Lowest: {0}C on {1}'.format(str(myreport.lowest_temp_val), myreport.lowest_temp_day))
        print('Humid: {0}% on {1}'.format(str(myreport.humidity_val), myreport.humidity_day))

    def display_average_report(self, myreport):
        print('Highest Average: {}C'.format(str(myreport.avg_highest_temp)))
        print('Lowest Average: {}C'.format(str(myreport.avg_lowest_temp)))
        print('Average Humidity: {}%'.format(str(myreport.avg_humidity)))

    def display_chart(self, myreport, flag):
        print(VariableFormatter.format_month_year(myreport))
        days = len(myreport.highest_temp)
        for num in range(0, days):
            (max_temp_val, min_temp_val,
             bar_max_temp, bar_min_temp,
             max_temp_red_str, min_temp_blue_str) = VariableFormatter.format_bars_and_temp_vals(myreport, num)
            num = num + 1
            date = VariableFormatter.change_to_two_digit(num)
            max_temp_val = VariableFormatter.change_to_two_digit(max_temp_val)
            min_temp_val = VariableFormatter.change_to_two_digit(min_temp_val)
            output_variables = {'date':date, 'max_temp_val':max_temp_val, 'min_temp_val':min_temp_val,
                                'bar_max_temp':bar_max_temp, 'bar_min_temp':bar_min_temp,
                                'max_temp_red_str':max_temp_red_str, 'min_temp_blue_str':min_temp_blue_str}
            VariableFormatter.print_formatted_chart(output_variables, flag)


class DataExtractor():
    @staticmethod
    def acquire_files(dir_path, year, full_month_name):
        all_files = os.listdir(dir_path)
        required_files = []
        for files in all_files:
            if year in files:
                if full_month_name in files:
                    required_files.append(files)
        if not required_files:
            print('Data for this month is not available')
            exit()
        return required_files

    @staticmethod
    def get_year_and_month(year_month):
        year_and_month = year_month.split('/')
        year = year_and_month[0]
        month = year_and_month[1]
        Validator.check_year_month(year,month)
        if len(month) == 2 and int(month) < 10:
            month = int(month)
        full_month_name = calendar.month_abbr[int(month)]
        return year, full_month_name


class VariableFormatter():
    @staticmethod
    def form_horizontal_bars(num):
        bar = ''
        if num is not None:
            for count in range(0, num):
                bar = '{}+'.format(bar)
        else:
            bar = None
        return bar

    @staticmethod
    def fetch_standard_month_name(filename):
        splited_file_name = filename.split('_')
        month_name = splited_file_name[3][0:3]
        month_name = calendar.month_name[time.strptime(month_name, '%b')[1]]
        return month_name

    @staticmethod
    def format_date(date):
        return time.strftime('%B %d',time.strptime(date, '%Y-%m-%d'))

    @staticmethod
    def change_to_two_digit(one_digit_num):
        if one_digit_num is not None:
            return str(one_digit_num).zfill(2)

    @staticmethod
    def format_month_year(myreport):
        return ('{0} {1}'.format(myreport.month, str(myreport.year)))

    @staticmethod
    def format_bars_and_temp_vals(myreport, num):
        max_temp_val = myreport.highest_temp[num]
        bar_max_temp = VariableFormatter.form_horizontal_bars(max_temp_val)
        min_temp_val = myreport.lowest_temp[num]
        bar_min_temp = VariableFormatter.form_horizontal_bars(min_temp_val)
        max_temp_red_str = colored(bar_max_temp, 'red')
        min_temp_blue_str = colored(bar_min_temp, 'blue')
        return (max_temp_val, min_temp_val, bar_max_temp,
            bar_min_temp, max_temp_red_str, min_temp_blue_str)

    @staticmethod
    def print_formatted_chart(date_temp, flag):
        if flag:
            VariableFormatter.format_chart(date_temp['max_temp_red_str'],
                                                            date_temp['max_temp_val'],
                                                            date_temp['date'], date_temp['bar_max_temp'])
            VariableFormatter.format_chart(date_temp['min_temp_blue_str'],
                                                            date_temp['min_temp_val'],
                                                            date_temp['date'], date_temp['bar_min_temp'])
        else:
            max_temp_val = '{}C'.format(str(date_temp['max_temp_val']))
            min_temp_val = '{}C'.format(str(date_temp['min_temp_val']))
            if Validator.validate_bar(date_temp['bar_max_temp']):
                max_temp_val = 'no data available'
            if Validator.validate_bar(date_temp['bar_min_temp']):
                min_temp_val = 'no data available'
            print('{0} {1}{2} {3}-{4}'.format(date_temp['date'], date_temp['min_temp_blue_str'],
                                                date_temp['max_temp_red_str'],min_temp_val, max_temp_val))

    @staticmethod
    def format_chart(bar, temperature, date, no_data_bar):
        if Validator.validate_bar(no_data_bar):
            print('{0} {1}'.format(date, 'No data available'))
        else:
            print('{0} {1} {2}C'.format(date, bar, str(temperature)))


class Validator():
    @staticmethod
    def check_dirpath_exists(dir_path):
        if not os.path.exists(dir_path):
            print('Directory path does not exist')
            exit()

    @staticmethod
    def check_year_month(year, month):
        Validator.check_year(year)
        match_obj = re.match(r'\d', month, re.M|re.I)
        if match_obj is None:
            print('invalid month')
            exit()
        if len(month) > 2:
            print('invalid month format')
            exit()
        if int(month) not in list(range(1, 13)):
            print('invalid month')
            exit()

    @staticmethod
    def check_year(year):
        match_obj = re.match(r'\d{4}', year, re.M|re.I)
        if match_obj is None:
            print('invalid year')
            exit()

    @staticmethod
    def temperature_values_are_none(rows):
        if re.findall(r'(?:^<)',rows['PKT']):
            return True
        else:
            return False

    @staticmethod
    def validate_bar(bar):
        if bar is None:
            return True


class TemperatureValuesExtractor():
    def extract_extreme_vals(self, myreport, rows):
        maxtemp = rows['Max TemperatureC']
        if maxtemp != '' and int(maxtemp) > myreport.highest_temp_val:
            myreport.highest_temp_val = int(maxtemp)
            myreport.highest_temp_day = VariableFormatter.format_date(rows['PKT'])
        mintemp = rows['Min TemperatureC']
        if mintemp != '' and int(mintemp) < myreport.lowest_temp_val:
            myreport.lowest_temp_val = int(mintemp)
            myreport.lowest_temp_day = VariableFormatter.format_date(rows['PKT'])
        maxhumid = rows['Max Humidity']
        if maxhumid != '' and int(maxhumid) > myreport.humidity_val:
            myreport.humidity_val = int(maxhumid)
            myreport.humidity_day = VariableFormatter.format_date(rows['PKT'])
        return myreport

    def extract_average_vals(self, myreport, rows):
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

    def extract_chart_report_vals(self, myreport, rows):
        maxtemp = rows['Max TemperatureC']
        if maxtemp != '':
            myreport.highest_temp.append(int(maxtemp))
        else:
            myreport.highest_temp.append(None)
        mintemp = rows['Min TemperatureC']
        if mintemp != '':
            myreport.lowest_temp.append(int(mintemp))
        else:
            myreport.lowest_temp.append(None)
        return myreport


class WeatherReportGenerator():
    def generate_extreme_weathers_report(self, year, dir_path):
        Validator.check_year(year)
        all_files = os.listdir(dir_path)
        required_files = []
        for files in all_files:
            if year in files:
                required_files.append(files)
        report_obj = ReportFormer()
        myreport = report_obj.make_extreme_report(required_files, dir_path)
        display_obj = ReportDisplayer()
        display_obj.display_extreme_report(myreport)

    def generate_average_weathers_report(self, year_month, dir_path):
        year, full_month_name = DataAccumulator.get_year_and_month(year_month)
        required_files = DataAccumulator.acquire_files(dir_path, year, full_month_name)
        report_obj = ReportFormer()
        myreport = report_obj.make_average_report(required_files[0], dir_path)
        display_obj = ReportDisplayer()
        display_obj.display_average_report(myreport)

    def generate_weather_charts(self, year_month, dir_path, report_label):
        year, full_month_name = DataAccumulator.get_year_and_month(year_month)
        required_files = DataAccumulator.acquire_files(dir_path, year, full_month_name)
        report_obj = ReportFormer()
        myreport = report_obj.make_chart_report(required_files[0], dir_path, year)
        display_obj = ReportDisplayer()
        if report_label == '-c':
            display_obj.display_chart(myreport,True)
        elif report_label == '-b':
            display_obj.display_chart(myreport, False)


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
    Validator.check_dirpath_exists(dir_path)
    weather_report = WeatherReportGenerator()
    if args.extreme_report:
        weather_report.generate_extreme_weathers_report(args.extreme_report, dir_path)
    elif args.average_report:
        weather_report.generate_average_weathers_report(args.average_report, dir_path)
    elif args.doublechart_report:
        report_label = '-c'
        weather_report.generate_weather_charts(args.doublechart_report, dir_path, report_label)
    elif args.singlechart_report:
        report_label = '-b'
        weather_report.generate_weather_charts(args.singlechart_report, dir_path, report_label)
    else:
        print('No Report Label Matched')
        exit()


if __name__ == '__main__':
    main()
