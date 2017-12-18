import sys
import os
import operator
from datetime import datetime
import calendar
from termcolor import colored

def get_files_list(path):
    result = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return result

def calculate_avg(data_list):
	temp = [int(item[1]) for item in data_list]
	result = sum(temp)/len(temp)
	return result

def remove_empty_strings_in_dictionary(dic):
    result = dict((k, v) for k, v in dic.iteritems() if v)
    return result

def sort_dictionary(dic):
    dic = remove_empty_strings_in_dictionary(dic)
    result = sorted(dic.items(), key=operator.itemgetter(1))
    return result

def print_year_result(max_temp, min_temp, max_humidity):
    max_temp_date = datetime.strptime(max_temp[0], '%Y-%m-%d')
    min_temp_date = datetime.strptime(min_temp[0], '%Y-%m-%d')
    max_humid_date = datetime.strptime(max_humidity[0], '%Y-%m-%d')

    print "Highest: {}C on {} {}".format(max_temp[1], max_temp_date.strftime("%B"), max_temp_date.day)
    print "Lowest: {}C on {} {}".format(min_temp[1], min_temp_date.strftime("%B"), min_temp_date.day)
    print "Humid: {}% on {} {}".format(max_humidity[1], max_humid_date.strftime("%B"), max_humid_date.day)

def print_month_result(avg_max_temp, avg_min_temp, avg_max_humidity):

    print "Highest Average: {}C".format(avg_max_temp[1])
    print "Lowest Average: {}C".format(avg_min_temp[1])
    print "Average Humidity: {}%".format(avg_max_humidity)


def parse_files(files_list, files_path):
    highest_temp = {}
    highest_temp_list = []
    lowest_temp_list = []
    max_humidity_list = []
    lowest_temp = {}
    highest_humidity = {}

    os.chdir(files_path)
    for file in files_list:
        my_file = open(file)
        data = my_file.readlines()
        for index, item in enumerate(data):
            if index == 0:
                continue
            else:
                row = item.split(",")
                highest_temp[row[0]] = row[1]
                lowest_temp[row[0]] = row[3]
                highest_humidity[row[0]] = row[7]
        temp1 = sort_dictionary(highest_temp)
        temp2 = sort_dictionary(lowest_temp)
        temp3 = sort_dictionary(highest_humidity)
        highest_temp_list.append(max(temp1,key=lambda x:int(x[1])))
        lowest_temp_list.append(min(temp2,key=lambda x:int(x[1])))
        max_humidity_list.append(max(temp3,key=lambda x:int(x[1])))
        my_file.close()

    max_temp = max(highest_temp_list,key=lambda x:int(x[1]))
    min_temp = min(lowest_temp_list,key=lambda x:int(x[1]))
    max_humidity = max(max_humidity_list,key=lambda x:int(x[1]))
    print_year_result(max_temp, min_temp, max_humidity)

def parse_file(file, files_path, month):
    avg_highest_temp = {}
    avg_highest_humidity = {}
    avg_highest_temp_list = []
    avg_lowest_temp_list = []
    avg_humidity_list = []
    avg_lowest_temp = {}
    avg_humidity = {}

    os.chdir(files_path)
    my_file = open(file)
    data = my_file.readlines()

    for index, item in enumerate(data):
        if index == 0:
            continue
        else:
            row = item.split(",")
            avg_highest_temp[row[0]] = row[2]
            avg_lowest_temp[row[0]] = row[2]
            avg_highest_humidity[row[0]] = row[8]

    temp1 = sort_dictionary(avg_highest_temp)
    temp2 = sort_dictionary(avg_lowest_temp)
    temp3 = sort_dictionary(avg_highest_humidity)

    avg_max_temp = max(temp1,key=lambda x:int(x[1]))
    avg_min_temp = min(temp2,key=lambda x:int(x[1]))
    avg_max_humidity = calculate_avg(temp3)
    my_file.close()

    print_month_result(avg_max_temp, avg_min_temp, avg_max_humidity)

def monthly_bar_chart(file, files_path, month, year):
    print calendar.month_name[month] + " " + year

    os.chdir(files_path)
    my_file = open(file)
    data = my_file.readlines()
    for index, item in enumerate(data):
        if index == 0:
            continue
        else:
            row = item.split(",")
            temp = row[0].split('-')
            day = temp[len(temp) - 1]
            if row[1] != '' and row[3] != '':
	            print_colored_chart(day, int(row[1]), "red")
	            print_colored_chart(day, int(row[3]), "blue")
    my_file.close()

def monthly_bar_bonus_chart(file, files_path, month, year):
    print calendar.month_name[month] + " " + year

    os.chdir(files_path)
    my_file = open(file)
    data = my_file.readlines()
    for index, item in enumerate(data):
        if index == 0:
            continue
        else:
            row = item.split(",")
            temp = row[0].split('-')
            day = temp[len(temp) - 1]
            if row[1] != '' and row[3] != '':
	            print_bonus_color_chart(day, int(row[1]), int(row[3]), 'red', 'blue')
    my_file.close()

def print_bonus_color_chart(day, high_temp, low_temp, color1, color2):
	count1 = 0
	count2 = 0
	print(day),
	while(count1 < high_temp):
		print colored('+', color1),
		count1 = count1 + 1
	while(count2 < low_temp):
		print colored('+', color2),
		count2 = count2 + 1
	print "{} - {} C".format(high_temp, low_temp)

def print_colored_chart(day, limit, color):
	count = 0
	print(day),
	while(count < limit):
		print colored('+', color),
		count = count + 1
	print "{} C".format(count)

def process_files(files_list, date, files_path, arguments):
    year_files = []

    temp = date.split("/")
    if len(temp) > 1:
        required_year = temp[0]
        month = int(temp[1])
        if month <=12:
            required_month = calendar.month_abbr[month]
    elif len(temp) == 1:
        required_year = temp[0]
    else:
        print "Invalid arguments."
        return


    for file in files_list:
        file_arguments = file.split('_')
        if (len(file_arguments) == 4 and len(temp) == 1 and file_arguments[2] == required_year):
            year_files.append(file)
        elif(len(file_arguments) == 4 and len(temp) == 2 and file_arguments[2] == required_year and month <=12):
            file_month = file_arguments[3].split('.')
            if file_month[0] == required_month:
                month_file = file

    if(len(temp) == 1 and arguments[1] == '-e'):
        parse_files(year_files, files_path)
    elif (len(temp) == 2 and month <=12 and arguments[1] == '-a'):
        parse_file(month_file, files_path, required_month)
    elif (len(temp) == 2 and month <=12 and arguments[1] == '-c'):
        monthly_bar_chart(month_file, files_path, month, required_year)
    elif (len(temp) == 2 and month <=12 and arguments[1] == '-d'):
        monthly_bar_bonus_chart(month_file, files_path, month, required_year)
    else:
        print "Invalid arguments."

def main():
    arguments = sys.argv
    path = os.path.abspath(arguments[len(arguments) - 1])
    files_list = get_files_list(path)
    process_files(files_list, arguments[2], path, arguments)


if __name__ == "__main__":
    main()