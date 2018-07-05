import os
import sys
from termcolor import colored

readings = {}
months_ = {1: "January", 2: "February", 3: "March", 4: "April",
           5: "May", 6: "June", 7: "July", 8: "August",
           9: "September", 10: "October", 11: "November", 12: "December"}


def parse_files(directory):
    year = 0
    month = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if(filename.endswith(".txt")):
            with open(os.path.join(directory, file)) as f:
                features = f.readline().split(",")[1:]
                day = 0
                daywise_dict = {}
                for line in f:
                    features_dict = {}
                    feature_values = line.split(",")
                    if(feature_values[0].strip() != ""):
                        year, month, day = feature_values[0].split("-")
                    feature_values = feature_values[1:]
                    for i in range(len(features)):
                        features_dict[features[i].strip()
                                      ] = feature_values[i].rstrip().strip()
                    daywise_dict[day] = features_dict
                readings.setdefault(year, {})[month] = daywise_dict


def readings_of_year(year):
    max_t = 0
    min_t = float('Inf')
    max_humid = 0
    max_t_day = ""
    min_t_day = ""
    max_humid_day = ""
    for month in readings[year].keys():
        for day in readings[year][month].keys():
            if(readings[year][month][day]["Max TemperatureC"] != ""):
                if(int(readings[year][month][day]["Max TemperatureC"]) >
                   max_t):
                    max_t = int(readings[year][month][day]["Max TemperatureC"])
                    max_t_day = months_[int(month)] + " " + day
            if(readings[year][month][day]["Min TemperatureC"] != ""):
                if(int(readings[year][month][day]["Min TemperatureC"]) <
                   min_t):
                    min_t = int(readings[year][month][day]["Min TemperatureC"])
                    min_t_day = months_[int(month)] + " " + day
            if(readings[year][month][day]["Max Humidity"] != ""):
                if(int(readings[year][month][day]["Max Humidity"]) >
                   max_humid):
                    max_humid = int(readings[year][month][day]["Max Humidity"])
                    max_humid_day = months_[int(month)] + " " + day
    print('Highest: ', max_t, "C on ", max_t_day, '\nLowest: ',
          min_t, "C on ", min_t_day, '\nHumidity: ', max_humid,
          "% on ", max_humid_day, sep='')


def average_of_month(month):
    year, month = month.split("/")
    days = len(readings[year][month].keys())

    max_t = [int(readings[year][month][day]["Max TemperatureC"])
             for day in readings[year][month].keys()
             if readings[year][month][day]["Max TemperatureC"] != ""]

    min_t = [int(readings[year][month][day]["Min TemperatureC"])
             for day in readings[year][month].keys()
             if readings[year][month][day]["Min TemperatureC"] != ""]

    mean_humidity = [int(readings[year][month][day]["Mean Humidity"])
                     for day in readings[year][month].keys()
                     if readings[year][month][day]["Mean Humidity"] != ""]

    max_t = int(sum(max_t) / int(days))
    min_t = int(sum(min_t) / int(days))
    mean_humidity = int(sum(mean_humidity) / int(days))

    print('Highest Average: ', max_t, "C\n", 'Lowest Average: ',
          min_t, "C\n", 'Average Mean Humidity: ', mean_humidity, "%", sep='')


def print_chart(day, max, min):
    if(max == ""):
        max = "0"
    if(min == ""):
        min = "0"
    print (colored(int(day), 'magenta'), ' ', colored('+' * int(min), 'blue'),
           colored('+' * int(max), 'red'), ' ', colored(int(min), 'magenta'),
           colored('C - ', 'magenta'), colored(int(max), 'magenta'),
           colored('C', 'magenta'), sep='')


def charts(month):
    year, month = month.split("/")
    for day in readings[year][month].keys():
        print_chart(day, readings[year][month][day]["Max TemperatureC"],
                    readings[year][month][day]["Min TemperatureC"])


def main():
    parse_files(sys.argv[1])
    if(len(sys.argv) >= 4):
        if(sys.argv[2] == "-a"):
            average_of_month(sys.argv[3])
        elif (sys.argv[2] == "-c"):
            charts(sys.argv[3])
        elif (sys.argv[2] == "-e"):
            readings_of_year(sys.argv[3])
        else:
            print("Invalid arguments")
    if(len(sys.argv) >= 6):
        if(sys.argv[4] == "-a"):
            average_of_month(sys.argv[5])
        elif (sys.argv[4] == "-c"):
            charts(sys.argv[5])
        elif (sys.argv[4] == "-e"):
            readings_of_year(sys.argv[5])
        else:
            print("Invalid arguments")
    if(len(sys.argv) >= 8):
        if(sys.argv[6] == "-a"):
            average_of_month(sys.argv[7])
        elif (sys.argv[6] == "-c"):
            charts(sys.argv[7])
        elif (sys.argv[6] == "-e"):
            readings_of_year(sys.argv[7])
        else:
            print("Invalid arguments")
if __name__ == "__main__":
    main()