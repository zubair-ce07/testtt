import calendar
import os
import re
from termcolor import colored

# Global Variables and containers for data storage

path = ''
file_names = []
month_files = []
max_temp_monthwise = []
low_temp_monthwise = []
date_monthwise = []
humid = []

# getting path of data files


def get_path():
    try:
        file = open(os.getcwd()+'/path',"r")
        path_string = file.read()
        path = path_string.strip()
        return path

    except Exception as e:
        print(e + '\nPlease place your path file in the same directory'
                  ' with the code file in phycharm default location')

# clearing Global Variables after use


def clear_variables():
    file_names.clear()
    month_files.clear()
    max_temp_monthwise.clear()
    low_temp_monthwise.clear()
    date_monthwise.clear()
    humid.clear()

# getting a specific year files


def get_files(year):
    global path
    try:
        for files in os.listdir(path):
            if re.match('.*' + year + '.*', files):
                file_names.append(files)
        print(os.listdir(path))
    except:
        print('Files not found for this year')

# getting a specific month file


def get_single_file(year, month):
    try:
        for files in os.listdir(path):
            if re.match('.*' + year + '.*', files):
                file_names.append(files)

        for _month in file_names:
            if re.match('.*' + month + '.*', _month):
                month_files.append(_month)
    except:
        print('File not found for this month')

# reading data from year files


def read_from_files():
    for my_file in file_names:
        _file = (open(path + my_file, 'r'))
        for line in _file:
            collection = line.split(',')
            if collection[1] == '' or collection[3] == '' or collection[7] == '':
                continue
            max_temp_monthwise.append(collection[1])
            low_temp_monthwise.append(collection[3])
            humid.append(collection[7])
            date_monthwise.append(collection[0])

# reading data from file for a month


def read_month_file():
    for my_file in month_files:
        file1 = (open(path + my_file,'r'))
        for line in file1:
            collection = line.split(',')
            if collection[1] == '' or collection[3] == '' or collection[7] == '':
                continue
            max_temp_monthwise.append(collection[1])
            low_temp_monthwise.append(collection[3])
            humid.append(collection[7])
            date_monthwise.append(collection[0])

# removing unnecessary elements(headers) from year files' container


def removing_elements():
    a = 0
    while a < len(file_names):
        max_temp_monthwise.remove('Max TemperatureC')
        low_temp_monthwise.remove('Min TemperatureC')
        humid.remove('Max Humidity')
        if 'PKT' in date_monthwise:
            date_monthwise.remove('PKT')
        else:
            date_monthwise.remove('PKST')
        a += 1

# removing unnecessary element(headers) from month file container


def removing_element():
    if len(month_files) > 0:
        max_temp_monthwise.remove('Max TemperatureC')
        low_temp_monthwise.remove('Min TemperatureC')
        humid.remove('Max Humidity')
        if 'PKT' in date_monthwise:
            date_monthwise.remove('PKT')
        else:
            date_monthwise.remove('PKST')
        temp_list_conversion()
    else:
        print('File not found for this month')

# Converting max_temp_monthwise into integer list


def temp_list_conversion():
    global max_temp_monthwise
    global low_temp_monthwise
    global humid
    max_temp_monthwise = list(map(int, max_temp_monthwise))
    low_temp_monthwise = list(map(int, low_temp_monthwise))
    humid = list(map(int, humid))

# for average maximum, minimum temperature and maximum average humidity


def show_average():
    global max_temp_monthwise
    global low_temp_monthwise
    global humid
    sum_max_temp = sum(max_temp_monthwise)
    sum_low_temp = sum(low_temp_monthwise)
    sum_humid = sum(humid)
    average_max_temp = int(sum_max_temp / len(max_temp_monthwise))
    average_low_temp = int(sum_low_temp / len(low_temp_monthwise))
    average_humid = int(sum_humid / len(humid))
    print('************************************')
    print('Highest Average: ' + str(average_max_temp) + 'C')
    print('Lowest Average: ' + str(average_low_temp) + 'C')
    print('Average Humidity: ' + str(average_humid) + '%')
    print('************************************')

# Date Conversion


def date_conversion(index):
    raw_date = index
    raw_date = raw_date.split('-')
    complete_date = calendar.month_name[int(raw_date[1])]
    complete_date = complete_date + " " + raw_date[2]
    return complete_date

# Print required information


def print_data():
    max_value = max(max_temp_monthwise)
    min_value = min(low_temp_monthwise)
    max_humid = max(humid)
    index = max_temp_monthwise.index(max_value)
    min_index = low_temp_monthwise.index(min_value)
    humid_index = humid.index(max_humid)
    print('************************************')
    print('Highest: ' + str(max_temp_monthwise[index]) + 'C on ' + date_conversion(date_monthwise[index]))
    print('Lowest: ' + str(low_temp_monthwise[min_index]) + 'C on ' + date_conversion(date_monthwise[min_index]))
    print('Humidity: ' + str(humid[humid_index]) + '% on ' + date_conversion(date_monthwise[humid_index]))
    print('************************************')

# Print chart


def print_chart():
    for a, b, c in zip(max_temp_monthwise, low_temp_monthwise, date_monthwise):
        print(c + colored('+'*a, 'red') + str(a) + 'C')
        print(c + colored('+'*b, 'blue') + str(b) + 'C')

# Bonus Task: Print both charts (bar charts) together


def print_bar_chart():
    for a, b, c in zip(max_temp_monthwise, low_temp_monthwise, date_monthwise):
        print(c + colored('+'*b, 'blue') + colored('+'*a, 'red') + str(b) + 'C ' + str(a) + 'C')

# Main Method


def main():
    global path
    path = get_path()
    print(path)
    while True:
        try:
            choice = int(input('Press 1 for year base information\nPress 2 for Month base information\n'
                               'Press 3 to print chart\nPress 4 to make horizontal bar chart for each day\n'
                               'Press 5 exit: '))
            if choice == 1:
                year = str(input('Enter the year you want to get information: '))
                get_files(year)
                read_from_files()
                removing_elements()
                temp_list_conversion()
                print_data()

            elif choice == 2:
                year = str(input('Enter the year you want to get information: '))
                month = str(input('Enter the month (i.e Jan): '))
                get_single_file(year, month)
                read_month_file()
                removing_element()
                show_average()

            elif choice == 3:
                year = str(input('Enter the year you want to get information: '))
                month = str(input('Enter the month (i.e Jan): '))
                get_single_file(year, month)
                read_month_file()
                removing_element()
                print_chart()

            elif choice == 4:
                year = str(input('Enter the year you want to get information: '))
                month = str(input('Enter the month (i.e Jan): '))
                get_single_file(year, month)
                read_month_file()
                removing_element()
                print_bar_chart()

            elif choice == 5:
                break

            else:
                print('Wrong choice')

            clear_variables()
            choice = 0
            print("\n")

        except Exception as e:
            print(e)
            clear_variables()
            choice = 0

# execution point of program


if __name__ == '__main__':
    main()