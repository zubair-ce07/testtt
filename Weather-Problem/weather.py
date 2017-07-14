import os
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-e', '--task1', type=str, help='Task-1', required=False, default=None)
parser.add_argument('-a', '--task2', type=str, help='Task-2', required=False, default=None)
parser.add_argument('-c', '--task3', type=str, help='Task-3', required=False, default=None)
args = parser.parse_args()

files = os.listdir('weatherfiles/')

months = [
          'Jan', 'Feb', 'Mar',
          'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep',
          'Oct', 'Nov', 'Dec'
         ]

def task1(year):
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
    list_vals = []


    for file_ in year_files:
        weather_file = open('weatherfiles/' + file_)
        lines = weather_file.readlines()

        for i in range(1,len(lines)):

            list_vals = lines[i].split(',')
            if list_vals[1] != '': 
                if max_temp < int(list_vals[1]):
                    max_temp = int(list_vals[1])
                    max_temp_date = list_vals[0]
            if list_vals[3] != '': 
                if min_temp < int(list_vals[3]):
                    min_temp = int(list_vals[3])
                    min_temp_date = list_vals[0]
            if list_vals[7] != '': 
                if max_humid < float(list_vals[7]):
                    max_humid = float(list_vals[7])
                    max_humid_date = list_vals[0]
        weather_file.close()
    print 'Highest: {}C on {} {}'.format(max_temp, months[int(max_temp_date.split('-')[1])-1], max_temp_date.split('-')[2])
    print 'Lowest: {}C on {} {}'.format(min_temp, months[int(min_temp_date.split('-')[1])-1], min_temp_date.split('-')[2])
    print 'Humidity: {}% on {} {}'.format(max_humid, months[int(max_humid_date.split('-')[1])-1], max_humid_date.split('-')[2])
    print '\n\n'


def task2(year, month):
    print 'Report:2 for month of {}, {}\n'.format(months[int(month)-1],year)
    weather_file = open('weatherfiles/Murree_weather_' + year + '_' +months[int(month)-1]+'.txt')
    lines = weather_file.readlines()
    avg_htemp = 0
    avg_mhum = 0
    avg_ltemp = 0
    avg_mhum = 0
    list_vals = []
    for i in range(1,len(lines)):
        list_vals = lines[i].split(',')
        if list_vals[1] != '':
            avg_htemp += int(list_vals[1])
        if list_vals[3] != '':
            avg_ltemp += int(list_vals[3])
        if list_vals[8] != '':
            avg_mhum += int(list_vals[8])
    avg_htemp /= len(lines)-1
    avg_ltemp /= len(lines)-1
    avg_mhum /= len(lines)-1
    print 'Highest Average: {}C'.format(avg_htemp)
    print 'Lowest Average: {}C'.format(avg_ltemp)
    print 'Average Mean Humidity: {}%'.format(avg_mhum)
    weather_file.close()
    print '\n\n'


def task3(year, month):
    print 'Report:3 for month of {}, {}\n'.format(months[int(month)-1],year)
    weather_file = open('weatherfiles/Murree_weather_' + year + '_' +months[int(month)-1]+'.txt')
    lines = weather_file.readlines()
    max_temp = 0
    min_temp = 0
    blue = '\033[94m'
    red = '\033[91m'
    list_vals = []
    for i in range(1,len(lines)):
        list_vals = lines[i].split(',')
        if list_vals[1] != '' and list_vals[3] != '':
            max_temp = int(list_vals[1])
            string_red = '+' * max_temp
            min_temp = int(list_vals[3])
            string_blue = '+' * min_temp
            print '{:0>2} {} {}{}{} \033[97m {}C - {}C'.format(i, blue, string_blue, red, string_red, min_temp, max_temp)
    weather_file.close()

task_1 = args.task1
task_2 = args.task2
task_3 = args.task3

if task_1 is not None:
    task1(task_1)

if task_2 is not None:
    task2(task_2.split('/')[0], task_2.split('/')[1])

if task_3 is not None:
    task3(task_3.split('/')[0], task_3.split('/')[1])