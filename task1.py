from argparse import ArgumentParser

import csv
import os
import fnmatch
import datetime


class WeatherReport:
    def __init__(self):
        self.years = dict()

    def parser(self,
               dir_name):
        for file_path in os.listdir(dir_name):
            if fnmatch.fnmatch(file_path, '*.txt'):
                filename = os.path.splitext(file_path)[0]
                year_month_names = filename.split('_')
                if year_month_names[2] not in self.years:
                    self.years[year_month_names[2]] = list()
                with open(dir_name + file_path, 'r') as csvfile:
                    month = Month(year_month_names[3])
                    reader = csv.DictReader(csvfile)
                    min_data = normalize_data(reader)
                    csvfile.seek(0)
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row is not '':
                            if row['Max TemperatureC'] is '':
                                row['Max TemperatureC'] \
                                    = int(min_data['avg_max_temp'])
                            if row['Min TemperatureC'] is '':
                                row['Min TemperatureC'] \
                                    = int(min_data['avg_min_temp'])
                            if row['Max Humidity'] is '':
                                row['Max Humidity'] \
                                    = int(min_data['avg_max_humidity'])
                            if row[' Mean Humidity'] is '':
                                row[' Mean Humidity'] \
                                    = int(min_data['avg_max_humidity'])
                            if 'PKT' in row:
                                day_num = row['PKT'].split('-')[2]
                            else:
                                day_num = row['PKST'].split('-')[2]
                            day = Day(day_num, row)
                            month.add_day(day)
                self.years[year_month_names[2]].append(month)

    def return_years(self):
        return self.years

    def yearly_report(self,
                      year):
        months = self.years[year]
        max_temp_dates = list()
        min_temp_dates = list()
        max_hum_dates = list()
        max_temp_list = list()
        min_temp_list = list()
        max_hum_list = list()

        for month in months:
            max_obj_list = monthly_high_low(month.days_list)
            max_temp_list.append(max_obj_list[0].max_temperature)
            min_temp_list.append(max_obj_list[1].min_temperature)
            max_hum_list.append(max_obj_list[2].max_humidity)
            max_temp_dates.append([max_obj_list[0].day_num, month.month_name])
            min_temp_dates.append([max_obj_list[1].day_num, month.month_name])
            max_hum_dates.append([max_obj_list[2].day_num, month.month_name])

        max_temp = max(max_temp_list)
        min_temp = min(min_temp_list)
        max_hum = max(max_hum_list)
        index_max_temp = max_temp_list.index(max_temp)
        index_min_temp = min_temp_list.index(min_temp)
        index_max_hum = max_hum_list.index(max_hum)
        print('Highest: {}C on {} {}'.format(max_temp,
                                             max_temp_dates[index_max_temp][1],
                                             max_temp_dates[index_max_temp][0])
              )

        print('Lowest: {}C on {} {}'.format(min_temp,
                                            min_temp_dates[index_min_temp][1],
                                            min_temp_dates[index_min_temp][0])
              )

        print('Highest: {}% on {} {}'.format(max_hum,
                                             max_hum_dates[index_max_hum][1],
                                             max_hum_dates[index_max_hum][0])
              )

    def monthly_report(self,
                       year,
                       month):
        months = self.years[year]
        result = list()
        for m in months:
            if m.month_name == month:
                result = monthly_avg_high_low(m.days_list)
        if result:
            print('Highest Average: {}C'.format(round(result[0])))
            print('Lowest Average: {}C'.format(round(result[1])))
            print('Average Mean Humidity: {}%'.format(round(result[2])))

    def daily_report(self,
                     year,
                     month):
        months = self.years[year]
        for m in months:
            if m.month_name == month:
                for day in m.days_list:
                    print(day.day_num.zfill(2), end=' ')
                    print('\033[1;34m', end='')
                    for i in range(round(int(day.min_temperature))):
                        print('+', end='')
                    print('\033[1;31m', end='')
                    for i in range(round(int(day.max_temperature))):
                        print('+', end='')
                    print('\033[1;39m', end='')
                    print(' {}C - {}C'.format(day.min_temperature,
                                              day.max_temperature))


class Year:
    def __init__(self,
                 y,
                 m):
        self.year_name = y
        self.months_list = [m]

    def get_year_name(self):
        return self.year_name

    def add_month(self,
                  m):
        self.months_list.append(m)


class Month:
    def __init__(self,
                 m):
        self.month_name = m
        self.days_list = list()

    def add_day(self,
                d):
        self.days_list.append(d)


class Day:

    def __init__(self,
                 d,
                 attr):
        self.day_num = d
        self.max_temperature = int(attr['Max TemperatureC'])
        self.min_temperature = int(attr['Min TemperatureC'])
        self.max_humidity = int(attr['Max Humidity'])
        self.mean_humidity = int(attr[' Mean Humidity'])


def normalize_data(reader):
    sum_max_temp = 0
    sum_min_temp = 0
    sum_max_humidity = 0
    sum_mean_humidity = 0
    for values in reader:
        if values['Max TemperatureC'] is not '':
            sum_max_temp += int(values['Max TemperatureC'])
        if values['Min TemperatureC'] is not '':
            sum_min_temp += int(values['Min TemperatureC'])
        if values['Max Humidity'] is not '':
            sum_max_humidity += int(values['Max Humidity'])
        if values[' Mean Humidity'] is not '':
            sum_mean_humidity += int(values[' Mean Humidity'])
        total_days = reader.__sizeof__() - 1
        result = dict()
        result['avg_max_temp'] = sum_max_temp/total_days
        result['avg_min_temp'] = sum_min_temp/total_days
        result['avg_max_humidity'] = sum_max_humidity/total_days
        result['avg_mean_humidity'] = sum_mean_humidity/total_days
    return result


def monthly_high_low(days_list):
    result = list()
    result.append(max(days_list, key=lambda day: day.max_temperature))
    result.append(min(days_list, key=lambda day: day.min_temperature))
    result.append(max(days_list, key=lambda day: day.max_humidity))
    return result


def monthly_avg_high_low(days_list):
    result = list()
    result.append(sum(day.max_temperature for day in days_list)/len(days_list))
    result.append(sum(day.min_temperature for day in days_list)/len(days_list))
    result.append(sum(day.mean_humidity for day in days_list)/len(days_list))
    return result


def get_month_num(month):
    return datetime.datetime.strptime(month,
                                      '%b').strftime('%m')


def get_month_name(month):
    return datetime.datetime.strptime(str(month),
                                      '%m').strftime('%b')


def determine_year(raw_year):
    raw_year = str(raw_year)
    years = raw_year.split('/')
    return years


def main():
    arg_parser = ArgumentParser(description='Process some integer')
    arg_parser.add_argument('path', type=str, nargs='+',
                            help='Collect the data from Directory')
    arg_parser.add_argument('-e', type=str, nargs='+',
                            help='Find the highest temperature and day, '
                                 'lowest temperature and day, most humid day '
                                 '(Single Month)')
    arg_parser.add_argument('-a', type=str, nargs='+',
                            help='Find the average highest temperature,'
                                 ' average lowest temperature, average mean '
                                 'humidity (Range of Months)')
    arg_parser.add_argument('-c', type=str, nargs='+',
                            help='Draws two horizontal bar charts for the'
                                 ' highest and lowest temperature on each  '
                                 'day. Highest in  red and lowest in blue. ('
                                 'Range of Months)')
    args = arg_parser.parse_args()
    wr = WeatherReport()
    print(args.path[0])
    wr.parser(args.path[0])
    try:
        if args.e:
            years = determine_year(args.e[0])
            wr.yearly_report(years[0])

        if args.a:
            years = determine_year(args.a[0])
            wr.monthly_report(years[0], get_month_name(years[1]))

        if args.c:
            years = determine_year(args.c[0])
            wr.daily_report(years[0], get_month_name(years[1]))

    except KeyError:
        print("Invalid Input")


if __name__ == "__main__":
    main()
