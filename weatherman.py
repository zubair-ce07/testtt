import os
import sys
from termcolor import colored
from datetime import date


def parse_files(directory):
    year = 0
    month = 0
    readings = {}
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if(filename.endswith(".txt")):
            with open(os.path.join(directory, file)) as csv_file:
                features = csv_file.readline().split(",")[1:]
                day = 0
                readings_for_a_day = {}
                for line in csv_file:
                    features_dict = {}
                    feature_values = line.split(",")
                    if feature_values[0].strip():
                        year, month, day = feature_values[0].split("-")
                    feature_values = feature_values[1:]
                    for i in range(len(features)):
                        features_dict[features[i].strip()
                                      ] = feature_values[i].strip()
                    readings_for_a_day[day] = features_dict
                readings.setdefault(year, {})[month] = readings_for_a_day
    return readings


def readings_of_year(year, readings):
    max_t = 0
    min_t = float('Inf')
    max_humid = 0
    max_t_day = ""
    min_t_day = ""
    max_humid_day = ""
    for month in readings[year].keys():
        for day in readings[year][month].keys():
            if(readings[year][month][day]["Max TemperatureC"]):
                if(int(readings[year][month][day]["Max TemperatureC"]) >
                   max_t):
                    max_t = int(readings[year][month][day]["Max TemperatureC"])
                    max_t_day = date(int(year), int(month),
                                     int(day)).ctime()[:-14]
            if(readings[year][month][day]["Min TemperatureC"]):
                if(int(readings[year][month][day]["Min TemperatureC"]) <
                   min_t):
                    min_t = int(readings[year][month][day]["Min TemperatureC"])
                    min_t_day = date(int(year), int(month),
                                     int(day)).ctime()[:-14]
            if(readings[year][month][day]["Max Humidity"]):
                if(int(readings[year][month][day]["Max Humidity"]) >
                   max_humid):
                    max_humid = int(readings[year][month][day]["Max Humidity"])
                    max_humid_day = date(int(year), int(month),
                                         int(day)).ctime()[:-14]
    print('Highest: ', max_t, "C on ", max_t_day, '\nLowest: ',
          min_t, "C on ", min_t_day, '\nHumidity: ', max_humid,
          "% on ", max_humid_day, sep='')


def average_of_date(date, readings):
    year, month = date.split("/")
    day_records = readings[year][month]

    max_temp = [int(day_records[day]["Max TemperatureC"])
                for day in day_records.keys()
                if readings[year][month][day]["Max TemperatureC"]]

    min_temp = [int(day_records[day]["Min TemperatureC"])
                for day in day_records.keys()
                if day_records[day]["Min TemperatureC"]]

    mean_humidity = [int(day_records[day]["Mean Humidity"])
                     for day in day_records.keys()
                     if day_records[day]["Mean Humidity"]]

    max_mean_temp = int(sum(max_temp) / len(day_records))
    min_mean_temp = int(sum(min_temp) / len(day_records))
    average_mean_humidity = int(sum(mean_humidity) / len(day_records))

    print('Highest Average: ', max_mean_temp, "C\n", 'Lowest Average: ',
          min_mean_temp, "C\n", 'Average Mean Humidity: ',
          average_mean_humidity, "%", sep='')
    # f"Highest Average: {max_mean_temp}C\nLowest Average: {min_mean_temp}\
    #  C\nAverage Mean Humidity: {average_mean_humidity}"


def print_chart(day, max, min):
    if(max == ""):
        max = "0"
    if(min == ""):
        min = "0"
    print (u'\u001b[35m', int(day), '\u001b[34m+' * int(min),
           '\u001b[31m+' * int(max), '\u001b[35m ', int(min),
           'C - ', int(max), 'C\u001b[0m', sep='')


def charts(month, readings):
    year, month = month.split("/")
    for day in readings[year][month].keys():
        print_chart(day, readings[year][month][day]["Max TemperatureC"],
                    readings[year][month][day]["Min TemperatureC"])


def main():

    readings = parse_files(sys.argv[1])
    if(len(sys.argv) >= 4):
        if(sys.argv[2] == "-a"):
            average_of_date(sys.argv[3], readings)
        elif (sys.argv[2] == "-c"):
            charts(sys.argv[3], readings)
        elif (sys.argv[2] == "-e"):
            readings_of_year(sys.argv[3], readings)
        else:
            print("Invalid arguments")
    if(len(sys.argv) >= 6):
        if(sys.argv[4] == "-a"):
            average_of_date(sys.argv[5], readings)
        elif (sys.argv[4] == "-c"):
            charts(sys.argv[5], readings)
        elif (sys.argv[4] == "-e"):
            readings_of_year(sys.argv[5], readings)
        else:
            print("Invalid arguments")
    if(len(sys.argv) >= 8):
        if(sys.argv[6] == "-a"):
            average_of_date(sys.argv[7], readings)
        elif (sys.argv[6] == "-c"):
            charts(sys.argv[7], readings)
        elif (sys.argv[6] == "-e"):
            readings_of_year(sys.argv[7], readings)
        else:
            print("Invalid arguments")
if __name__ == "__main__":
    main()
