import sys
import csv
import os.path
from datetime import datetime
import re

MIN_VALUE = -35565
MAX_VALUE = 35565
ZERO = 0


class TemperatureOfYear:
    """ This is a class for storing Yearly Temperature """
    def __init__(self, high=MIN_VALUE, low=MAX_VALUE, hum=ZERO):
        self.highest = high
        self.highest_temp_day = ""
        self.lowest = low
        self.lowest_temp_day = ""
        self.humidity = hum
        self.humid_day = ""


class AverageTemperatue:
    """ Class for storing Average Temperatures """
    def __init__(self, high=ZERO, low=ZERO, hum=ZERO):
        self.avg_high = high
        self.avg_low = low
        self.avg_humidity = hum


MONTHS_NAME = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

MONTHS_ABBR = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}
FILE_START_NAME = "Murree_weather_"
FILE_EXTENSION = ".txt"
input_val = sys.argv[1]


def find_yearly_temperature(file_path, yearly_temperatue):
    if os.path.exists(file_path):
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
    else:
        return False


def get_formatted_date(date_str):
    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d")
    return formatted_date


def find_average_temperature(file_path):
    if os.path.exists(file_path):
        # yearly_temperatue = TemperatureOfYear()
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
        avg_temp = AverageTemperatue()
        avg_temp.avg_high = average_high / high_count
        avg_temp.avg_low = average_low / low_count
        avg_temp.avg_humidity = average_humid / humid_count
        return avg_temp
    else:
        return False


def display_daily_temperature(file_path):
    if os.path.exists(file_path):
        with open(file_path) as csvfile:
            read_csv = csv.DictReader(csvfile, delimiter=',')
            for row in read_csv:
                day = row['PKT'].split("-")[2]
                if row['Max TemperatureC'] != '':
                    max_temp = int(row['Max TemperatureC'])
                    max_temp_string = ""
                    for x in range(max_temp):
                        max_temp_string = max_temp_string + "+"
                    print("%s \033[0;31m%s\033[0;m %dC" % (day, max_temp_string, max_temp))
                if row['Min TemperatureC'] != '':
                    min_temp = int(row['Min TemperatureC'])
                    min_temp_string = ""
                    for x in range(min_temp):
                        min_temp_string = min_temp_string + "-"
                    print("%s \033[0;34m%s\033[0;m %dC" % (day, min_temp_string, min_temp))
        return True
    else:
        return False


def disp_daily_temp_horizontal(file_path):
    if os.path.exists(file_path):
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
        return True
    else:
        return False

args_length = len(sys.argv)
if args_length != 4:
    print("Invalid Arguments")
    print("Please Provide Arguments as shown below: ")
    print("weatherman.py -e 2005/5 /path/to/files")
    exit(-1)
if bool(re.search("^-.$", sys.argv[1])) == False:
    print("Second Argument must be in the form '-*'")
    exit(-1)
if bool(re.search("^\d{4}(([/])(0?[1-9]|1[012]))?$", sys.argv[2])) == False:
    print("Third Argument must be in the form 'YYYY' OR 'YYYY/MM'")
    exit(-1)
if os.path.exists(sys.argv[3]) == False:
    print("Please provide Valid path of Data Directory")
    exit(-1)
if input_val == "-e":
    date = sys.argv[2].split('/')
    year = date[0]
    dir_path = sys.argv[3]
    yearly_temperatue = TemperatureOfYear()
    for x in range(1, 13):
        path = dir_path+"/"+FILE_START_NAME+year+"_"+MONTHS_ABBR[x]+FILE_EXTENSION
        ret_val = find_yearly_temperature(path, yearly_temperatue)
        if ret_val != False:
            ret_val = yearly_temperatue
    if yearly_temperatue.highest != MIN_VALUE:
        print("Highest: %dC on %s" % (
            yearly_temperatue.highest,
            get_formatted_date(yearly_temperatue.highest_temp_day)))
    else:
        print("No Record of Highest Temperature Found for This Year")
    if yearly_temperatue.lowest != MAX_VALUE:
        print("Lowest: %dC on %s" % (
            yearly_temperatue.lowest,
            get_formatted_date(yearly_temperatue.lowest_temp_day)))
    else:
        print("No Record of Lowest Temperature Found for This Year")
    if yearly_temperatue.humid_day != "":
        print("Humid: %d%% on %s" % (
            yearly_temperatue.humidity,
            get_formatted_date(yearly_temperatue.humid_day)))
    else:
        print("No Record of Humidity Found for This Year")
elif input_val == "-a":
    if bool(re.search("^\d{4}([/])(0?[1-9]|1[012])$", sys.argv[2])) == False:
        print("Date should be of the form 'YYYY/MM'")
        exit(-1)
    date = sys.argv[2].split('/')
    year = date[0]
    month = int(date[1])
    dir_path = sys.argv[3]
    path = dir_path + "/" + FILE_START_NAME + year \
           + "_" + MONTHS_ABBR[month] + FILE_EXTENSION
    avg_temp = AverageTemperatue()
    ret_val = find_average_temperature(path)
    if ret_val != False:
        avg_temp = ret_val
        print("%s %s" % (MONTHS_NAME[month], year))
        print("Highest Average: %dC" % avg_temp.avg_high)
        print("Lowest Average: %dC" % avg_temp.avg_low)
        print("Average Humidity: %d%%" % avg_temp.avg_humidity)
    else:
        print("No data found for specified date")
elif input_val == "-c":
    if bool(re.search("^\d{4}([/])(0?[1-9]|1[012])$", sys.argv[2])) == False:
        print("Date should be of the form 'YYYY/MM'")
        exit(-1)
    date = sys.argv[2].split('/')
    year = date[0]
    month = int(date[1])
    dir_path = sys.argv[3]
    path = dir_path + "/" + FILE_START_NAME + year + "_" + MONTHS_ABBR[month] + FILE_EXTENSION
    print("%s %s" % (MONTHS_NAME[month], year))
    ret_val = display_daily_temperature(path)
    if ret_val == False:
        print("No data found for specified date")
elif input_val == "-h":
    if bool(re.search("^\d{4}([/])(0?[1-9]|1[012])$", sys.argv[2])) == False:
        print("Date should be of the form 'YYYY/MM'")
        exit(-1)
    date = sys.argv[2].split('/')
    year = date[0]
    month = int(date[1])
    dir_path = sys.argv[3]
    path = dir_path + "/" + FILE_START_NAME + year + "_" + MONTHS_ABBR[month] + FILE_EXTENSION
    print("%s %s" % (MONTHS_NAME[month], year))
    ret_val = disp_daily_temp_horizontal(path)
    if ret_val == False:
        print("No data found for specified date")
else:
    print("Invalid Input")
    print("Give 2nd argument")
    print("'-e' for yearly report")
    print("'-a' for monthly report")
    print("'-c for monthly report in separate charts'")