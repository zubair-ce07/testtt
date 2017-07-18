import os
import sys
import csv
import argparse

def year_check(value):
    if int(value) < 2003 or int(value) > 2017:
        raise argparse.ArgumentTypeError("Year Should be Between 2004 and 2016")
    else:
        return value

def year_month_check(value):
    try:
        year,month =  value.split('/')
    except Exception as e:
        raise argparse.ArgumentTypeError("Input should be in Year/Month Format")
    year_check(year)
    if int(month) < 1 or int(month) > 12:
        raise argparse.ArgumentTypeError("Invalid Month value, Month should be Between 01-12")
    else:
        return value

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--annual_weather_extremes', type=year_check, help='Annual Weather Extremes', required=False, default=None)
parser.add_argument('-a', '--monthly_average_weather', type=year_month_check, help='Montly Average Weather', required=False, default=None)
parser.add_argument('-c', '--daily_weather_extremes', type=year_month_check, help='Daily Weather extremes of Specifies Month', required=False, default=None)
parser.add_argument('file_path', help='Directory to data, use relative path like dir/to/files')
args = parser.parse_args()


report_1 = args.annual_weather_extremes
report_2 = args.monthly_average_weather
report_3 = args.daily_weather_extremes
file_path = args.file_path

files = os.listdir(file_path)

months = [
          'Jan', 'Feb', 'Mar',
          'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep',
          'Oct', 'Nov', 'Dec'
         ]

def annual_weather_extremes(year):
    print 'Report: 1 for the Year: {} \n'.format(year)
    year_files = []
    for file_ in files:
        if file_.find(year) > 0:
            year_files.append(file_)
    max_temp = 0
    max_temp_date = None
    min_temp = 0
    min_temp_date = None
    max_humid = 0
    max_humid_date = None
    max_temp_month = []
    min_temp_month = []
    max_humid_month = []

    for file_ in year_files:
        weather_file = open(file_path + '/' + file_)
        reader = csv.DictReader(weather_file)
        list_of_dicts = [x for x in reader if x['Max TemperatureC'] != "" or x['Min TemperatureC'] != "" or x['Max Humidity'] != "" ]
        max_temp_month.append(max(list_of_dicts, key=lambda x: int(x['Max TemperatureC'])))
        min_temp_month.append(min(list_of_dicts, key=lambda x: int(x['Min TemperatureC'])))
        max_humid_month.append(max(list_of_dicts, key=lambda x: int(x['Max Humidity'])))
        weather_file.close()


    max_temp = max(max_temp_month, key=lambda x: int(x['Max TemperatureC']))
    min_temp = min(min_temp_month, key=lambda x: int(x['Min TemperatureC']))
    max_humid = max(max_humid_month, key=lambda x: int(x['Max Humidity']))

    month_highest_temp = months[int(max_temp['PKT'].split('-')[1])-1]
    month_lowest_temp = months[int(min_temp['PKT'].split('-')[1])-1]
    month_max_humid = months[int(max_humid['PKT'].split('-')[1])-1]

    print 'Highest: {}C on {} {}'.format(max_temp['Max TemperatureC'], month_highest_temp, max_temp['PKT'].split('-')[2])
    print 'Lowest: {}C on {} {}'.format(min_temp['Min TemperatureC'], month_lowest_temp, min_temp['PKT'].split('-')[2])
    print 'Humidity: {}% on {} {}'.format(max_humid['Max Humidity'], month_max_humid, max_humid['PKT'].split('-')[2])
    print '\n\n'


def monthly_average_weather(year, month):
    print 'Report:2 for month of {}, {}\n'.format(months[int(month)-1],year)
    weather_file = open(file_path + '/Murree_weather_' + year + '_' +months[int(month)-1]+'.txt')
    avg_htemp = 0
    avg_mhum = 0
    avg_ltemp = 0
    avg_mhum = 0
    list_vals = []
    row_count = 0
    reader = csv.DictReader(weather_file)

    for line in reader:
        row_count += 1
        if line['Max TemperatureC'] != '':
            avg_htemp += int(line['Max TemperatureC'])
        if line['Min TemperatureC'] != '':
            avg_ltemp += int(line['Min TemperatureC'])
        if line[' Mean Humidity'] != '':
            avg_mhum += int(line[' Mean Humidity'])

    avg_htemp /= row_count
    avg_ltemp /= row_count
    avg_mhum /= row_count
    print 'Highest Average: {}C'.format(avg_htemp)
    print 'Lowest Average: {}C'.format(avg_ltemp)
    print 'Average Mean Humidity: {}%'.format(avg_mhum)
    weather_file.close()
    print '\n\n'


def daily_weather_extremes(year, month):
    print 'Report:3 for month of {}, {}\n'.format(months[int(month)-1],year)
    weather_file = open(file_path + '/Murree_weather_' + year + '_' +months[int(month)-1]+'.txt')
    max_temp = 0
    min_temp = 0
    blue = '\033[94m'
    red = '\033[91m'
    row_count = 0
    reader = csv.DictReader(weather_file)
    for line in reader:
        row_count += 1
        if line['Max TemperatureC'] != '' and  line['Min TemperatureC'] != '':
            max_temp = int(line['Max TemperatureC'])
            string_red = '+' * max_temp
            min_temp = int(line['Min TemperatureC'])
            string_blue = '+' * min_temp
            print '{:0>2} {} {}{}{} \033[97m {}C - {}C'.format(row_count, blue, string_blue, red, string_red, min_temp, max_temp)
    weather_file.close()


if os.path.exists(file_path):

    if not (report_1 or report_2 or report_3):
        parser.error('No action requested, add -e followed by Year or -a/-c followed by year/month')

    if report_1 is not None:
        annual_weather_extremes(report_1)

    if report_2 is not None:
        year, month = report_2.split("/")
        monthly_average_weather(year, month)

    if report_3 is not None:
        year, month = report_3.split("/")
        daily_weather_extremes(year, month)
else:
    print "Directory {} doesn't exists".format(file_path)
