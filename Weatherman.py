import sys
import argparse
import csv
import calendar
import glob
import operator
import os
import re


class Weather:
    """weather object to store a days weather"""

    def __init__(self, date, month, year, max_temp, min_temp, max_humidity, mean_humidity):
        self.Date = date
        self.Month = month
        self.Year = year
        self.Max_Temp = max_temp
        self.Min_Temp = min_temp
        self.Max_Humidity = max_humidity
        self.Mean_Humidity = mean_humidity


weather_records = []

# dividing date into separate values of day month and year
def dividing_date(date):
    date = date.split("-")
    return date[2], calendar.month_abbr[int(date[1])], date[0]


# reading the files needed for the user requirement and maintaining a record
def read_files(file_path):
    files = glob.glob(file_path)
    for file in files:
        with open(file) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if 'PKST' in row.keys():
                    row['PKT'] = row['PKST']
                    del row['PKST']
                day, month, year = dividing_date(row['PKT'])

                # catering for empty values
                if row['Min TemperatureC'] == "":
                    row['Min TemperatureC'] = "0.000001"
                if row['Max TemperatureC'] == "":
                    row['Max TemperatureC'] = "0.000001"
                if row['Max Humidity'] == "":
                    row['Max Humidity'] = "0.000001"
                if row[' Mean Humidity'] == "":
                    row[' Mean Humidity'] = "0.000001"

                weather_records.append(
                    Weather(int(day), month, int(year), float(row['Max TemperatureC']), float(row['Min TemperatureC']),
                            float(row['Max Humidity']), float(row[' Mean Humidity'])))

    return weather_records


# calculating yearly summary of max temp, min temp and max humidiity
def year_info(year):
    year_records = []
    for record in weather_records:
        if record.Year == year:
            year_records.append(record)

    # calculating min max mean
    max_temp_day = max(year_records, key=operator.attrgetter('Max_Temp'))
    max_humid_day = max(year_records, key=operator.attrgetter('Max_Humidity'))
    min_temp_day = min(year_records, key=operator.attrgetter('Min_Temp'))

    # printing as required
    print("Highest : " + str(int(max_temp_day.Max_Temp)) + "C on " + str(max_temp_day.Month) + " " + str(max_temp_day.Date))

    print("Lowest : " + str(int(min_temp_day.Min_Temp)) + "C on " + str(min_temp_day.Month) + " " + str(min_temp_day.Date))

    print("Humidity : " + str(int(max_humid_day.Max_Humidity)) + "C on " + str(max_humid_day.Month) + " " + str(max_humid_day.Date))

    print("")


# calculating monthly summary
def month_info(month, year):

    month_records = []
    zero_added_in_min_temp = 0
    zero_added_in_max_temp = 0
    zero_added_in_mean_humid = 0

    for record in weather_records:
        if record.Year == year and record.Month == month:
            if record.Min_Temp == 0.000001:
                zero_added_in_min_temp += 1
            if record.Max_Temp == 0.000001:
                zero_added_in_max_temp += 1
            if record.Mean_Humidity == 0.000001:
                zero_added_in_mean_humid += 1
            month_records.append(record)

    # calculating averages
    max_temp_day = sum(record.Max_Temp for record in month_records) / (len(month_records) - zero_added_in_max_temp)
    mean_humid_day = sum(record.Mean_Humidity for record in month_records) / (len(month_records) - zero_added_in_mean_humid)
    min_temp_day = sum(record.Min_Temp for record in month_records) / (len(month_records) - zero_added_in_min_temp)

    # printing as required
    print("Highest Temperature Average : " + str(int(max_temp_day)) + "C")
    print("Lowest Temperature Average : " + str(int(min_temp_day)) + "C")
    print("Average Mean humidity : " + str(int(mean_humid_day)) + "%")
    print("")


# displaying monthly graph
def month_graph(month, year):

    month_records = []
    for record in weather_records:
        if record.Year == year and record.Month == month:
            month_records.append(record)

    i = 0
    # string to be printed
    symbol_str = "+"

    #  colors for graphs
    red = '\033[91m'
    blue = '\033[94m'
    grey = '\033[37m'

    # printing bar for each day in the month
    for d in month_records:
        if d.Min_Temp == 0 and d.Max_Temp == 0:
            print("no record found")
        else:
            print(str(d.Date) + " " + blue + symbol_str * int(d.Min_Temp) + red + symbol_str * (
                int(d.Max_Temp) - int(d.Min_Temp)) + grey + "  " +
                  str(int(d.Min_Temp)) + "-" + str(int(d.Max_Temp)) + "C")
    print("")


def main(argv):

    # regex to check input
    regex = r"(\d{4})/(\d{1,2})"

    # creating and parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("Directory", help="Path to record Directory e.g weatherfiles/weatherfiles/")
    parser.add_argument("-e", "--yearInfo", action='append',
                        help="give the year you want the record of e.g. 2008", type=int)
    parser.add_argument("-a", "--monthInfo", action='append',
                        help="give the month and year you want record of e.g. 2008/4")
    parser.add_argument("-c", "--monthGraph", action='append',
                        help="give the month and year you want graph of e.g. 2008/4")
    args = parser.parse_args()


    if args.Directory:
        if os.path.isdir(args.Directory):
            file_path = args.Directory + "*.txt"
            read_files(file_path)
        else:
            print("Illegal Path")

    if args.yearInfo is not None:
        for x in args.yearInfo:
            if 1900 > x > 3000:
                print("please enter a viable year")
            else:
                year_info(x)

    if args.monthInfo is not None:
        for x in args.monthInfo:
            match = re.match(regex, x)
            if match is not None:
                month_info(calendar.month_abbr[int(match.group(2))], int(match.group(1)))
            else:
                print ("please enter correct month format")

    if args.monthGraph is not None:
        for x in args.monthGraph:
            match = re.match(regex, x)
            if match is not None:
                month_graph(calendar.month_abbr[int(match.group(2))], int(match.group(1)))
            else:
                print("please enter correct month format")


if __name__ == "__main__":
    main(sys.argv[1:])
