import sys
import csv
import os.path
from datetime import datetime
import re
import constants
from yearlytemperature import TemperatureOfYear
from averagetemp import AverageTemperatue


def find_yearly_temperature(file_path, yearly_temperatue):
    """
    This function take a valid file_path and an object of TemperatureOfYear
    and return TemperatureOfYear object having updated temperatue
    """
    with open(file_path) as csvfile:
        read_csv = csv.DictReader(csvfile, delimiter=',')
        for row in read_csv:
            if row['Max TemperatureC'] != '':
                hight_temp = int(row['Max TemperatureC'])
                if hight_temp > yearly_temperatue.highest:
                    yearly_temperatue.highest = hight_temp
                    yearly_temperatue.highest_temp_day = row['PKT']
            if row['Min TemperatureC'] != '':
                low_temp = int(row['Min TemperatureC'])
                if low_temp < yearly_temperatue.lowest:
                    yearly_temperatue.lowest = low_temp
                    yearly_temperatue.lowest_temp_day = row['PKT']
            if row['Max Humidity'] != '':
                humidity = int(row['Max Humidity'])
                if humidity > yearly_temperatue.humidity:
                    yearly_temperatue.humidity = humidity
                    yearly_temperatue.humid_day = row['PKT']
    return yearly_temperatue


def get_formatted_date(date_str):
    """
    This function accepts a string and return a required formatted sate string
    """
    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d")
    return formatted_date


def find_average_temperature(file_path):
    """
    This function take file path and return the
    AverageTemperature object
    """
    average_high = 0
    average_low = 0
    average_humid = 0
    high_count = 0
    low_count = 0
    humid_count = 0
    with open(file_path) as csvfile:
        read_csv = csv.DictReader(csvfile, delimiter=',')
        for row in read_csv:
            if row['Max TemperatureC'] != '':
                average_high = average_high + int(row['Max TemperatureC'])
                high_count = high_count + 1
            if row['Min TemperatureC'] != '':
                average_low = average_low + int(row['Min TemperatureC'])
                low_count = low_count + 1
            if row[' Mean Humidity'] != '':
                average_humid = average_humid + int(row[' Mean Humidity'])
                humid_count = humid_count + 1
    avg_temperature = AverageTemperatue()
    avg_temperature.avg_high = average_high / high_count
    avg_temperature.avg_low = average_low / low_count
    avg_temperature.avg_humidity = average_humid / humid_count
    return avg_temperature


def display_daily_temperature(file_path):
    """
    :param file_path:
    :return: none
    displays the daily temperture of a month
    """
    with open(file_path) as csvfile:
        read_csv = csv.DictReader(csvfile, delimiter=',')
        for row in read_csv:
            day = row['PKT'].split("-")[2]
            if row['Max TemperatureC'] != '':
                max_temp = int(row['Max TemperatureC'])
                max_temp_string = ""
                for index in range(max_temp):
                    max_temp_string = max_temp_string + "+"
                print("%s \033[0;31m%s\033[0;m %dC" % (day, max_temp_string, max_temp))
            if row['Min TemperatureC'] != '':
                min_temp = int(row['Min TemperatureC'])
                min_temp_string = ""
                for index in range(min_temp):
                    min_temp_string = min_temp_string + "-"
                print("%s \033[0;34m%s\033[0;m %dC" % (day, min_temp_string, min_temp))


def disp_daily_temp_horizontal(file_path):
    """
    :param file_path:
    :return: none
    display horizontally the temperatures of the month
    """
    with open(file_path) as csvfile:
        read_csv = csv.DictReader(csvfile, delimiter=',')
        for row in read_csv:
            max_temp_flag = False
            min_temp_flag = False
            day = row['PKT'].split("-")[2]
            if row['Max TemperatureC'] != '':
                max_temp = int(row['Max TemperatureC'])
                max_temp_string = ""
                max_temp_flag = True
                for x in range(max_temp):
                    max_temp_string = max_temp_string + "+"
            if row['Min TemperatureC'] != '':
                min_temp = int(row['Min TemperatureC'])
                min_temp_string = ""
                min_temp_flag = True
                for x in range(min_temp):
                    min_temp_string = min_temp_string + "-"
            if max_temp_flag or min_temp_flag:
                print("%s \033[0;34m%s\033[0;m\033[0;31m%s\033[0;m  %dC - %dC"
                      % (day, min_temp_string, max_temp_string,
                         min_temp, max_temp))


input_val = sys.argv[1]
args_length = len(sys.argv)
if args_length != 4:
    print("Invalid Arguments")
    print("Please Provide Arguments as shown below: ")
    print("weatherman.py -e 2005/5 /path/to/files")
    exit(-1)
if bool(re.search("^-.$", sys.argv[1])) is False:
    print("Second Argument must be in the form '-*'")
    exit(-1)
if bool(re.search("^\d{4}(([/])(0?[1-9]|1[012]))?$", sys.argv[2])) is False:
    print("Third Argument must be in the form 'YYYY' OR 'YYYY/MM'")
    exit(-1)
if os.path.exists(sys.argv[3]) is False:
    print("Please provide Valid path of Data Directory")
    exit(-1)
if input_val == "-e":
    date = sys.argv[2].split('/')
    year = date[0]
    dir_path = sys.argv[3]
    yearly_temp = TemperatureOfYear()
    for x in range(1, 13):
        path = dir_path+"/"+constants.FILE_START_NAME+year+"_"+\
               constants.MONTHS_ABBR[x]+constants.FILE_EXTENSION
        if os.path.exists(path):
            yearly_temp = find_yearly_temperature(path, yearly_temp)

    if yearly_temp.highest != constants.MIN_VALUE:
        print("Highest: %dC on %s" % (
            yearly_temp.highest,
            get_formatted_date(yearly_temp.highest_temp_day)))
    else:
        print("No Record of Highest Temperature Found for This Year")
    if yearly_temp.lowest != constants.MAX_VALUE:
        print("Lowest: %dC on %s" % (
            yearly_temp.lowest,
            get_formatted_date(yearly_temp.lowest_temp_day)))
    else:
        print("No Record of Lowest Temperature Found for This Year")
    if yearly_temp.humid_day != "":
        print("Humid: %d%% on %s" % (
            yearly_temp.humidity,
            get_formatted_date(yearly_temp.humid_day)))
    else:
        print("No Record of Humidity Found for This Year")
elif input_val == "-a":
    if bool(re.search("^\d{4}([/])(0?[1-9]|1[012])$", sys.argv[2])) is False:
        print("Date should be of the form 'YYYY/MM'")
        exit(-1)
    date = sys.argv[2].split('/')
    year = date[0]
    month = int(date[1])
    dir_path = sys.argv[3]
    path = dir_path + "/" + constants.FILE_START_NAME + year \
           + "_" + constants.MONTHS_ABBR[month] + constants.FILE_EXTENSION
    if os.path.exists(path):
        avg_temp = find_average_temperature(path)

        print("%s %s" % (constants.MONTHS_NAME[month], year))
        print("Highest Average: %dC" % avg_temp.avg_high)
        print("Lowest Average: %dC" % avg_temp.avg_low)
        print("Average Humidity: %d%%" % avg_temp.avg_humidity)
    else:
        print("No Data Found for the Specified Month")
elif input_val == "-c":
    if bool(re.search("^\d{4}([/])(0?[1-9]|1[012])$", sys.argv[2])) is False:
        print("Date should be of the form 'YYYY/MM'")
        exit(-1)
    date = sys.argv[2].split('/')
    year = date[0]
    month = int(date[1])
    dir_path = sys.argv[3]
    path = dir_path + "/" + constants.FILE_START_NAME + year + "_" \
           + constants.MONTHS_ABBR[month] + constants.FILE_EXTENSION
    if os.path.exists(path):
        print("%s %s" % (constants.MONTHS_NAME[month], year))
        display_daily_temperature(path)
    else:
        print("No Data Found for the Specified Month")
elif input_val == "-h":
    if bool(re.search("^\d{4}([/])(0?[1-9]|1[012])$", sys.argv[2])) is False:
        print("Date Should be of the Form 'YYYY/MM'")
        exit(-1)
    date = sys.argv[2].split('/')
    year = date[0]
    month = int(date[1])
    dir_path = sys.argv[3]
    path = dir_path + "/" + constants.FILE_START_NAME + year + "_" \
           + constants.MONTHS_ABBR[month] + constants.FILE_EXTENSION
    if os.path.exists(path):
        print("%s %s" % (constants.MONTHS_NAME[month], year))
        disp_daily_temp_horizontal(path)
    else:
        print("No Data Found for the Specified Month")
else:
    print("Invalid Input")
    print("Give 2nd argument")
    print("'-e' for yearly report")
    print("'-a' for monthly report")
    print("'-c for monthly report in separate charts'")
