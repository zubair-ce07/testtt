from argparse import ArgumentParser

import data_structure

import csv
import os
import fnmatch
import datetime




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
    wr = data_structure.WeatherReport()
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
