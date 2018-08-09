"""
This module read user input , read files , perform calculation and generate reports
"""
from datetime import datetime
import argparse
import os
import calendar


class WeatherReading:
    """The class holds each weather reading"""

    def __init__(self):
        self.highest_temp = 0
        self.lowest_temp = 0
        self.most_humidity = 0
        self.mean_humidity = 0
        self.date = 0

    def add_month_value(self, highest_tmp, lowest_tmp, most_humidity, mean_humidity, date):
        """The method stores  day data """
        self.highest_temp = highest_tmp
        self.lowest_temp = lowest_tmp
        self.most_humidity = most_humidity
        self.mean_humidity = mean_humidity
        self.date = date

    def view_day_data(self):
        """The method print  day data """
        print('date:', self.date)
        print('Max temp:', self.highest_temp)
        print('Min temp:', self.lowest_temp)
        print('Most humidity:', self.most_humidity)
        print('Mean humidity:', self.mean_humidity)
        print("\n")


class WeatherResults:
    """The class contains calculated weather results"""

    def __init__(self):
        self.maximum_temp_value = 0
        self.minimum_temp_value = 0
        self.most_humidity_value = 0
        self.max_temp_date = ''
        self.min_temp_date = ''
        self.most_humidity_date = ''
        self.average_maximum_temp = 0
        self.average_minimum_temp = 0
        self.average_mean_humidity = 0

    def set_weather_results_yearly(
            self, max_tmp, max_temp_date, min_tmp, min_temp_date, most_humidity_val, most_humidity_date):
        """The method populate the daily temperatures"""
        self.maximum_temp_value = max_tmp
        self.minimum_temp_value = min_tmp
        self.most_humidity_value = most_humidity_val
        self.max_temp_date = max_temp_date
        self.min_temp_date = min_temp_date
        self.most_humidity_date = most_humidity_date

    def set_weather_results_averages(self, avrg_max, avrg_min, avrg_mean_humid):
        """The method populate the average temperatures"""
        self.average_maximum_temp = avrg_max
        self.average_minimum_temp = avrg_min
        self.average_mean_humidity = avrg_mean_humid


class Report:
    """The class prints the report"""

    def year_report(self, result_object):
        """The method prints the report of year max min temp ,most humidity"""
        date_format = datetime.strptime(
            result_object.max_temp_date, '%Y-%m-%d')
        print(
            'Maximum: ', result_object.maximum_temp_value, 'C', 'on ', datetime.strftime(date_format, '%B %d'))
        date_format = datetime.strptime(
            result_object.min_temp_date, '%Y-%m-%d')
        print(
            'Lowest: ', result_object.minimum_temp_value, 'C', 'on ', datetime.strftime(date_format, '%B %d'))
        date_format = datetime.strptime(
            result_object.most_humidity_date, '%Y-%m-%d')
        print(
            'Humidity: ', result_object.most_humidity_value, '%', 'on ', datetime.strftime(date_format, '%B %d'))

    def month_average_report(self, result_object):
        """The method prints the average report of month max min temp ,mean humidity"""
        print('Highest Average: ', result_object.average_maximum_temp, 'C')
        print('Lowest Average: ', result_object.average_minimum_temp, 'C')
        print('Average Mean Humidity: ',
              result_object.average_mean_humidity, '%')

    def graphic_report(self, month_year, day_data_obj):
        """The method prints the graphic report of month max min temperature"""
        date_format = datetime.strptime(month_year, '%Y-%m-%d')
        print(
            datetime.strftime(date_format, '%B %Y'))
        for day in range(len(day_data_obj)):
            if day_data_obj[day].highest_temp == '' or day_data_obj[day].lowest_temp == '':
                print(day + 1, 'N/A')
                print(day + 1, 'N/A')
            else:
                convert_maxtmp_str_to_int = int(day_data_obj[day].highest_temp)
                convert_mintmp_str_to_int = int(day_data_obj[day].lowest_temp)
                ttl_plus_max = '+'*convert_maxtmp_str_to_int
                print(day + 1, '\033[1;31m', ttl_plus_max,
                      '\033[1;m', convert_maxtmp_str_to_int, 'C')

                ttl_plus_min = '+'*convert_mintmp_str_to_int
                print(day + 1, '\033[1;34m', ttl_plus_min,
                      '\033[1;m', convert_mintmp_str_to_int, 'C')
        print(
            '\n BONUS TASK')
        print(
            datetime.strftime(date_format, '%B %Y'))
        for day in range(len(day_data_obj)):
            if day_data_obj[day].highest_temp == '' or day_data_obj[day].lowest_temp == '':
                print(day + 1, 'N/A')
            else:
                convert_maxtmp_str_to_int = int(day_data_obj[day].highest_temp)
                convert_mintmp_str_to_int = int(day_data_obj[day].lowest_temp)
                ttl_plus_max = '+'*convert_maxtmp_str_to_int
                ttl_plus_min = '+'*convert_mintmp_str_to_int
                print(
                    day +
                    1, '\033[1;34m', ttl_plus_min, '\033[1;m', '\033[1;31m', ttl_plus_max, '\033[1;m',
                    convert_mintmp_str_to_int, 'C', '-', convert_maxtmp_str_to_int, 'C')


class DataCalculation:
    """The class gets data and perform calculations"""

    def calculate_yearly_month_max(self, day_data_obj):
        """The method find maximum,minimum temperature and most humidity"""
        max_temp = 0
        max_temp_date = ''
        min_temp = 0
        min_temp_date = ''
        most_humidity1 = 0
        most_humidity_date = ''
        min_count = 0
        for days in range(len(day_data_obj)):
            if (day_data_obj[days].highest_temp == '' or
                    day_data_obj[days].lowest_temp == '' or
                    day_data_obj[days].most_humidity == ''):
                continue
            else:
                if int(day_data_obj[days].highest_temp) > max_temp:
                    max_temp = int(day_data_obj[days].highest_temp)
                    max_temp_date = day_data_obj[days].date
                if min_count == 0:
                    min_temp = int(day_data_obj[days].lowest_temp)
                    min_temp_date = day_data_obj[days].date
                    min_count += 1
                else:
                    if int(day_data_obj[days].lowest_temp) < min_temp:
                        min_temp = int(day_data_obj[days].lowest_temp)
                        min_temp_date = day_data_obj[days].date
                if int(day_data_obj[days].most_humidity) > most_humidity1:
                    most_humidity1 = int(day_data_obj[days].most_humidity)
                    most_humidity_date = day_data_obj[days].date
        result_object = WeatherResults()
        result_object.set_weather_results_yearly(
            max_temp, max_temp_date, min_temp, min_temp_date, most_humidity1, most_humidity_date)
        report_object = Report()
        report_object.year_report(result_object)

    def calculate_averages(self, day_data_obj):
        """The method find average ofmaximum,minimum temperature and mean humidity"""
        sum_max_temp = 0
        avrg_max_tmp = 0
        sum_min_temp = 0
        avrg_min_tmp = 0
        sum_mean_humidity = 0
        avrg_mean_humidity = 0
        data_found_count = 0
        for days in range(len(day_data_obj)):
            if (day_data_obj[days].highest_temp == ''
                    or day_data_obj[days].lowest_temp == ''
                    or day_data_obj[days].mean_humidity == ''):
                continue
            else:
                sum_max_temp = sum_max_temp + \
                    int(day_data_obj[days].highest_temp)
                sum_min_temp = sum_min_temp + \
                    int(day_data_obj[days].lowest_temp)
                sum_mean_humidity = sum_mean_humidity + \
                    int(day_data_obj[days].mean_humidity)
                data_found_count += 1
        avrg_max_tmp = sum_max_temp / data_found_count
        avrg_min_tmp = sum_min_temp / data_found_count
        avrg_mean_humidity = sum_mean_humidity / data_found_count
        result_object = WeatherResults()
        result_object.set_weather_results_averages(
            avrg_max_tmp, avrg_min_tmp, avrg_mean_humidity)
        report_object = Report()
        report_object.month_average_report(result_object)

    def calculate_max_min(self, day_data_obj):
        """The method populate maximum,minimum temperature of month to report class"""
        month_year = day_data_obj[0].date
        report_object = Report()
        report_object.graphic_report(month_year, day_data_obj)


class FileParser:
    """The class filters the files"""

    def read_files(self, year_input, path_to_dir, type_of_report):
        """The method read the files"""
        month_count = 0
        file_name_list = []
        expr = year_input.find('/') > 0
        month_list = []
        if expr is True:
            split_month = year_input.split('/')
            convert_year_to_int = int(split_month[0])
            convert_month_to_int = int(split_month[1])
            year_converted = convert_year_to_int
            ttl_month = 1
            file_name = "Murree_weather_" + str(year_converted) + \
                "_" + calendar.month_abbr[convert_month_to_int] + ".txt"

            if os.path.isfile(path_to_dir + file_name):
                month_count = month_count + 1
                file_name_list.append(file_name)
                month_list.append(convert_month_to_int)
        else:
            year_converted = year_input
            for total_months in range(13):
                file_name = "Murree_weather_" + year_converted + \
                    "_" + calendar.month_abbr[total_months] + ".txt"

                if os.path.isfile(path_to_dir + file_name):
                    month_count = month_count + 1
                    file_name_list.append(file_name)
                    month_list.append(total_months)

            ttl_month = month_count
        count = 0
        count_month_days = 0
        sum_ = 0
        for data_insert in range(ttl_month):
            count_month_days = calendar.monthrange(
                int(year_converted), int(month_list[data_insert]))[1]
            sum_ = sum_ + count_month_days
        ttl_days = sum_
        day_index = 0
        day_data_objects = [None]*ttl_days

        for i in range(ttl_days):
            day_data_objects[i] = WeatherReading()

        for data_insert in range(month_count):
            count = 0
            file_get = file_name_list[data_insert]
            path2 = path_to_dir + file_get
            file_data1 = open(path2, "r")
            current_month_data = file_data1.read()
            count = calendar.monthrange(
                int(year_converted), int(month_list[data_insert]))[1]
            for month_num in range(count):
                pro_data = current_month_data.split('\n')
                day_data = pro_data[month_num + 1]
                day_pro_data = day_data.split(',', 9)
                max_tmp_val = 0
                min_tmp_val = 0
                most_humid_val = 0
                mean_humid_val = 0
                date3 = ''
                max_tmp_val = day_pro_data[1]
                min_tmp_val = day_pro_data[3]
                most_humid_val = day_pro_data[7]
                mean_humid_val = day_pro_data[8]
                date3 = day_pro_data[0]
                day_data_objects[day_index].add_month_value(
                    max_tmp_val, min_tmp_val, most_humid_val, mean_humid_val, date3)
                day_index += 1
        calculate = DataCalculation()
        if type_of_report == 1:
            calculate.calculate_yearly_month_max(day_data_objects)
        elif type_of_report == 2:
            calculate.calculate_averages(day_data_objects)
        elif type_of_report == 3:
            calculate.calculate_max_min(day_data_objects)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", help="enter the year", type=str)
    parser.add_argument("-a", help="enter the year", type=str)
    parser.add_argument("-c", help="enter the year", type=str)
    parser.add_argument("path", help="enter the year", type=str)
    args = parser.parse_args()
    read_file_object = FileParser()
    if args.e is not None:
        read_file_object.read_files(args.e, args.path, 1)
        print()
    if args.a is not None:
        read_file_object.read_files(args.a, args.path, 2)
        print()
    if args.c is not None:
        read_file_object.read_files(args.c, args.path, 3)
        print()
