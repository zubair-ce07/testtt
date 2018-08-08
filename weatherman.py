import sys
import csv
import os.path
from datetime import datetime

MIN_VALUE = -35565
MAX_VALUE = 35565
ZERO = 0

class TemperatureOfYear:
    # highest = MIN_VALUE
    # highest_temp_day = ""
    # lowest = MAX_VALUE
    # lowest_temp_day = ""
    # humidity = ZERO
    # humid_day = ""
    def __init__(self, high=MIN_VALUE, low=MAX_VALUE, hum=ZERO):
        self.highest = high
        self.highest_temp_day = ""
        self.lowest = low
        self.lowest_temp_day = ""
        self.humidity = hum
        self.humid_day = ""


class AverageTemperatue:
    def __init__(self, high=ZERO, low=ZERO, hum=ZERO):
        self.avg_high = high
        self.avg_low = low
        self.avg_humidity = hum


MONTHS_NAME = {
    1 : "January",
    2 : "February",
    3 : "March",
    4 : "April",
    5 : "May",
    6 : "June",
    7 : "July",
    8 : "August",
    9 : "September",
    10 : "October",
    11 : "November",
    12 : "December"
}

MONTHS_ABBR = {
    1 : "Jan",
    2 : "Feb",
    3 : "Mar",
    4 : "Apr",
    5 : "May",
    6 : "Jun",
    7 : "Jul",
    8 : "Aug",
    9 : "Sep",
    10 : "Oct",
    11 : "Nov",
    12 : "Dec"
}
FILE_START_NAME = "Murree_weather_"
FILE_EXTENSION = ".txt"
input_val = sys.argv[1]


def find_yearly_temperature(file_path, yearly_temperatue):
    if os.path.exists(file_path):
        # yearly_temperatue = TemperatureOfYear()
        with open(file_path) as csvfile:
            readCSV = csv.DictReader(csvfile, delimiter=',')
            for row in readCSV:
                if row['Max TemperatureC'] != '':
                    hight_temp = int(row['Max TemperatureC'])
                if row['Min TemperatureC'] != '':
                    low_temp = int(row['Min TemperatureC'])
                if row['Max Humidity'] != '':
                    humidity = int(row['Max Humidity'])
                # yearly_temperatue.set_values(hight_temp, low_temp, humidity)
                if hight_temp > yearly_temperatue.highest:
                    yearly_temperatue.highest = hight_temp
                    yearly_temperatue.highest_temp_day = row['PKT']

                if low_temp < yearly_temperatue.lowest:
                    yearly_temperatue.lowest = low_temp
                    yearly_temperatue.lowest_temp_day = row['PKT']

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
        average_high=0
        average_low = 0
        average_humid = 0;
        count=0
        with open(file_path) as csvfile:
            readCSV = csv.DictReader(csvfile, delimiter=',')
            for row in readCSV:
                if row['Max TemperatureC'] != '':
                    average_high = average_high + int(row['Max TemperatureC'])
                if row['Min TemperatureC'] != '':
                    average_low = average_low + int(row['Min TemperatureC'])
                if row[' Mean Humidity'] != '':
                    average_humid = average_humid + int(row[' Mean Humidity'])
                # yearly_temperatue.set_values(hight_temp, low_temp, humidity)
                count = count+1;
        avg_temp = AverageTemperatue()
        avg_temp.avg_high = average_high / count
        avg_temp.avg_low = average_low / count
        avg_temp.avg_humidity = average_humid / count
        return avg_temp
    else:
        return False

if input_val == "-e":
    year = sys.argv[2]
    dir_path = sys.argv[3]
    yearly_temperatue = TemperatureOfYear()
    for x in range(1, 13):
        path = dir_path+"/"+FILE_START_NAME+year+"_"+MONTHS_ABBR[x]+FILE_EXTENSION
        ret_val = find_yearly_temperature(path, yearly_temperatue)
        if ret_val != False:
            ret_val = yearly_temperatue
    print("Highest: %d on %s" % (yearly_temperatue.highest, get_formatted_date(yearly_temperatue.highest_temp_day)))
    print("Lowest: %d on %s" % (yearly_temperatue.lowest, get_formatted_date(yearly_temperatue.lowest_temp_day)))
    print("Humid: %d%% on %s" % (yearly_temperatue.humidity, get_formatted_date(yearly_temperatue.humid_day)))
elif input_val == "-a":
    date = sys.argv[2].split('/')
    year = date[0]
    month = int(date[1])
    # print(date)
    dir_path = sys.argv[3]
    path = dir_path + "/" + FILE_START_NAME + year + "_" + MONTHS_ABBR[month] + FILE_EXTENSION
    avg_temp = AverageTemperatue()
    ret_val = find_average_temperature(path)
    if ret_val != False:
        avg_temp = ret_val
    print("%s %s" % (MONTHS_NAME[month], year))
    print("Highest Average: %d" % avg_temp.avg_high)
    print("Lowest Average: %d" % avg_temp.avg_low)
    print("Average Humidity: %d" % avg_temp.avg_humidity)
else:
    print("invalid input")

