import argparse
import csv
import os


def parsing_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path of the weatherfiles")
    parser.add_argument("-e", "--extremes", action="store")
    parser.add_argument("-a", "--average", action="store")
    parser.add_argument("-c", "--charts", action="store")
    return parser.parse_args()


def print_daily_temperature(high, low, date):
    colors = {'red': '0;31;0', 'blue': '0;34;0'}
    input_text_high = ''
    input_text_low = ''
    for i in range(0, high, 1):
        input_text_high += '+'
    for i in range(0, low, 1):
        input_text_low += '+'
    input_text_high = '\x1b[%sm %s \x1b[0m' % (colors['red'], input_text_high)
    input_text_low = '\x1b[%sm %s \x1b[0m' % (colors['blue'], input_text_low)
    print(date + input_text_high + str(high) + 'C')
    print(date + input_text_low + str(low) + 'C')


def print_daily_temperature_bonus(high, low, date):
    colors = {'red': '0;31;0', 'blue': '0;34;0'}
    input_text_high = ''
    input_text_low = ''
    for i in range(0, high, 1):
        input_text_high += '+'
    for i in range(0, low, 1):
        input_text_low += '+'
    input_text_high = '\x1b[%sm%s\x1b[0m' % (colors['red'], input_text_high)
    input_text_low = '\x1b[%sm%s\x1b[0m' % (colors['blue'], input_text_low)
    print(date + ' ' + input_text_low + input_text_high + ' ' + str(low) + 'C - ' + str(high) + 'C')


def parsing_monthly_input(path, input_year_month):
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
              6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
              11: 'Nov', 12: 'Dec'}
    year_month = input_year_month.split('/')
    for file_name in os.listdir(path):
        if months[int(year_month[1])] in file_name and year_month[0] in file_name:
            return file_name
    return None


def parsing_yearly_input(path, year):
    file_names = []
    for file_name in os.listdir(path):
        if year in file_name:
            file_names.append(file_name)
    return file_names


def parse_date(date):
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
              6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October',
              11: 'November', 12: 'December'}
    date_elements = date.split('-')
    return months[int(date_elements[1])] + " " + date_elements[2]


def display_average(args):
    filename = parsing_monthly_input(args.path, args.average)
    data_sum = [0, 0, 0, 0, 0, 0]
    with open(args.path + '/' + filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Max TemperatureC']:
                data_sum[0] += int(row['Max TemperatureC'])
                data_sum[1] += 1
            if row['Min TemperatureC']:
                data_sum[2] += int(row['Min TemperatureC'])
                data_sum[3] += 1
            if row[' Mean Humidity']:
                data_sum[4] += int(row[' Mean Humidity'])
                data_sum[5] += 1
    print ("Highest Average: " + str(data_sum[0] / data_sum[1]) + 'C')
    print ("Lowest Average: " + str(data_sum[2] / data_sum[3]) + 'C')
    print ("Average Mean Humidity: " + str(data_sum[4] / data_sum[5]) + '%')


def display_extremes(args):
    files = parsing_yearly_input(args.path, args.extremes)
    max_temp = {'date': None, 'temperature': None}
    min_temp = {'date': None, 'temperature': None}
    max_humid = {'date': None, 'percentage': None}
    for filename in files:
        with open(args.path + '/' + filename, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not max_temp['date']:
                    max_temp['date'] = row['PKT']
                    min_temp['date'] = row['PKT']
                    max_humid['date'] = row['PKT']
                    max_temp['temperature'] = row['Max TemperatureC']
                    min_temp['temperature'] = row['Min TemperatureC']
                    max_humid['percentage'] = row['Max Humidity']
                else:
                    if row['Max TemperatureC']:
                        if int(max_temp['temperature']) < int(row['Max TemperatureC']):
                            max_temp['temperature'] = row['Max TemperatureC']
                            max_temp['date'] = row['PKT']
                    if row['Min TemperatureC']:
                        if int(min_temp['temperature']) > int(row['Min TemperatureC']):
                            min_temp['temperature'] = row['Min TemperatureC']
                            min_temp['date'] = row['PKT']
                    if row['Max Humidity']:
                        if int(max_humid['percentage']) < int(row['Max Humidity']):
                            max_humid['percentage'] = row['Max Humidity']
                            max_humid['date'] = row['PKT']
    print ("Highest: " + max_temp['temperature'] + 'C on ' + parse_date(max_temp['date']))
    print ("Lowest: " + min_temp['temperature'] + 'C on ' + parse_date(min_temp['date']))
    print ("Humidity: " + max_humid['percentage'] + '% on ' + parse_date(max_humid['date']))


def display_charts(args):
    filename = parsing_monthly_input(args.path, args.charts)
    with open(args.path + '/' + filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Max TemperatureC'] and row['Min TemperatureC']:
                print_daily_temperature(int(row['Max TemperatureC']), int(row['Min TemperatureC']),
                                        row['PKT'].split('-')[2])
                print_daily_temperature_bonus(int(row['Max TemperatureC']), int(row['Min TemperatureC']),
                                              row['PKT'].split('-')[2])


if __name__ == '__main__':
    arguments = parsing_arguments()
    if arguments.average:
        display_average(arguments)
    if arguments.extremes:
        display_extremes(arguments)
    if arguments.charts:
        display_charts(arguments)

# in average calculation, if a day does not contain the entry for the property
# that day is ignored for that property
