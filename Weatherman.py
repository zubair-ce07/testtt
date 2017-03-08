import sys
import argparse
import csv
import calendar
import glob
import operator
import os
import re


class WeatherRecord:
    """weather object to store a days weather"""

    def __init__(self, date, month, year, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = date
        self.month = month
        self.year = year
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity


# dividing date into separate values of day month and year
def dividing_date(date):
    date = date.split("-")
    return date[2], calendar.month_abbr[int(date[1])], date[0]


# reading the files needed for the user requirement and maintaining a record
def read_files(file_path):
    weather_records =[]
    files = glob.glob(file_path)
    for file in files:
        with open(file) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                day, month, year = dividing_date(row.get('PKT') or row.get('PKST'))

                # catering for empty values
                if not row['Min TemperatureC']:
                    row['Min TemperatureC'] = "0.000001"
                if not row['Max TemperatureC']:
                    row['Max TemperatureC'] = "0.000001"
                if not row['Max Humidity']:
                    row['Max Humidity'] = "0.000001"
                if not row[' Mean Humidity']:
                    row[' Mean Humidity'] = "0.000001"

                weather_records.append(
                    WeatherRecord(int(day), month, int(year), float(row['Max TemperatureC']),
                                  float(row['Min TemperatureC']), float(row['Max Humidity']), float(row[' Mean Humidity'])))

    return weather_records


# calculating yearly summary of max temp, min temp and max humidiity
def year_info(weather_records, year):
    year_records = []
    for record in weather_records:
        if record.year == year:
            year_records.append(record)

    # calculating min max mean

    max_temp_day = max(filter(lambda x: x.max_temp != 0.000001, year_records), key=operator.attrgetter('max_temp'))
    max_humid_day = max(filter(lambda x: x.max_humidity != 0.000001, year_records), key=operator.attrgetter('max_humidity'))
    min_temp_day = min(filter(lambda x: x.min_temp != 0.000001, year_records), key=operator.attrgetter('min_temp'))

    # printing as required
    print("Highest : {0:.0f}C on {1} {2}".format(max_temp_day.max_temp, max_temp_day.month, max_temp_day.date))
    print("Lowest : {0:.0f}C on {1} {2}".format(min_temp_day.min_temp, min_temp_day.month, min_temp_day.date))
    print("Humidity : {0:.0f}% on {1} {2}".format(max_humid_day.max_humidity, max_humid_day.month, max_humid_day.date))
    print("")


# calculating monthly summary
def month_info(weather_records, month, year):

    month_records = []
    zero_added_in_min_temp = 0
    zero_added_in_max_temp = 0
    zero_added_in_mean_humid = 0

    for record in weather_records:
        if record.year == year and record.month == month:
            if record.min_temp == 0.000001:
                zero_added_in_min_temp += 1
            if record.max_temp == 0.000001:
                zero_added_in_max_temp += 1
            if record.mean_humidity == 0.000001:
                zero_added_in_mean_humid += 1
            month_records.append(record)

    # calculating averages
    max_temp_day = sum(record.max_temp for record in month_records) / (len(month_records) - zero_added_in_max_temp)
    mean_humid_day = sum(record.mean_humidity for record in month_records) / (len(month_records) - zero_added_in_mean_humid)
    min_temp_day = sum(record.min_temp for record in month_records) / (len(month_records) - zero_added_in_min_temp)

    # printing as required
    print("Highest Temperature Average : {0:.0f}C".format(max_temp_day))
    print("Lowest Temperature Average : {0:.0f}C".format(min_temp_day))
    print("Average Mean humidity : {0:.0f}%".format(mean_humid_day))
    print("")


# displaying monthly graph
def month_graph(weather_records, month, year):

    month_records = []
    for record in weather_records:
        if record.year == year and record.month == month:
            month_records.append(record)

    #  colors for graphs
    red = '\033[91m'
    blue = '\033[94m'
    grey = '\033[37m'

    # printing bar for each day in the month
    for d in month_records:
        if d.min_temp == 0.000001 and d.max_temp == 0.000001:
            print("no record found")
        else:
            blue_str = "+" * int(d.min_temp)
            red_str = "+" * (int(d.max_temp) - int(d.min_temp))

            print("{} {}{}{}{} {}{:.0f}-{:.0f}C".format(d.date, blue, blue_str, red, red_str, grey, d.min_temp, d.max_temp ))

    print("")


def main():


    # regex to check input
    regex = r"(\d{4})/(\d{1,2})"

    # creating and parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Path to record Directory e.g weatherfiles/weatherfiles/")
    parser.add_argument("-e", "--year_info", action='append',
                        help="give the year you want the record of e.g. 2008", type=int)
    parser.add_argument("-a", "--month_info", action='append',
                        help="give the month and year you want record of e.g. 2008/4")
    parser.add_argument("-c", "--month_graph", action='append',
                        help="give the month and year you want graph of e.g. 2008/4")
    args = parser.parse_args()


    if args.directory:
        if os.path.isdir(args.directory):
            file_path = args.directory + "*.txt"
            weather_records = read_files(file_path)
        else:
            print("Invalid Path")

    if args.year_info:
        for y in args.year_info:
            if 1900 > y > 3000:
                print("please enter a viable year")
            else:
                year_info(weather_records, y)

    if args.month_info:
        for x in args.month_info:
            match = re.match(regex, x)
            if match:
                month_info(weather_records, calendar.month_abbr[int(match.group(2))], int(match.group(1)))
            else:
                print ("please enter correct month format e.g. 2008/4")

    if args.month_graph:
        for x in args.month_graph:
            match = re.match(regex, x)
            if match:
                month_graph(weather_records, calendar.month_abbr[int(match.group(2))], int(match.group(1)))
            else:
                print("please enter correct month format e.g. 2008/4")


if __name__ == "__main__":
    main()
