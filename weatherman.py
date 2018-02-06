# weather_man_task
from datetime import datetime
import glob
import operator
import re
import argparse
import csv
import os

# constants
HIGH_TEMP_COLOR = 31    # RED
LOW_TEMP_COLOR = 34     # BLUE
DEFAULT_COLOR = 37


# class for computing the calculations given the readings data structure.
class ComputingSubTaskResults:
    # Tasks Division
    def sub_task_1(self, year_value, path):
            read_reports = Reports()
            read_reports.fetch_high_low_temp_humidity_day(year_value, path)

    def sub_task_2(self, year_month_value, path):
        month_value = year_month_value
        month_value_split = month_value.split("/")
        date_converted = datetime.strptime(month_value_split[1], '%m')

        read_reports = Reports()
        read_reports.fetch_avg(month_value_split[0], date_converted.strftime("%b"), path)

    def sub_task_3(self, year_month_value, path):
        month_value = year_month_value
        month_value_split = month_value.split("/")
        date_converted = datetime.strptime(month_value_split[1], '%m')

        print("\n%s %s" % (date_converted.strftime("%B"), month_value_split[0]))

        read_reports = Reports()
        read_reports.draw_high_low_charts(month_value_split[0], date_converted.strftime("%b"), path)

    # Computation results
    def high_low_temp_and_day(self, files_yearly_parameter):
        save_high_temp_data, save_low_temp_data, save_humid_data = [], [], []
        data = {}

        for a in files_yearly_parameter:
            if a is not None:

                    for c in a:
                        if c is not None:
                            if c["max_temperature"] != '':
                                save_high_temp_data.append(int(c["max_temperature"]))
                                data[c["max_temperature"]] = c["pkt"]

                            if c["min_temperature"] != '':
                                save_low_temp_data.append(int(c["min_temperature"]))
                                data[c["min_temperature"]] = c["pkt"]

                            if c["max_humidity"] != '':
                                save_humid_data.append(int(c["max_humidity"]))
                                data[c["max_humidity"]] = c["pkt"]

        max_temp = max(save_high_temp_data) if save_high_temp_data.__len__() else 0
        min_temp = min(save_low_temp_data) if save_low_temp_data.__len__() else 0
        max_humid = max(save_humid_data) if save_humid_data.__len__() else 0

        high_date_converted = datetime.strptime(data.get('%s' % max_temp), '%Y-%m-%d')
        low_date_converted = datetime.strptime(data.get('%s' % min_temp), '%Y-%m-%d')
        humid_date_converted = datetime.strptime(data.get('%s' % max_humid), '%Y-%m-%d')

        print('\nHighest: %sC on %s %d' % (max_temp, high_date_converted.strftime("%B"),
                                           high_date_converted.day))
        print('Lowest: %sC on %s %d' % (min_temp, low_date_converted.strftime("%B"),
                                        low_date_converted.day))
        print('Humidity: %s%% on %s %d' % (max_humid, humid_date_converted.strftime("%B"),
                                           humid_date_converted.day))

    def avg_high_temp(self, files_yearly_parameter):
        high_temp_data, low_temp_data, mean_humidity_data = [], [], []
        for a in files_yearly_parameter:
            if a is not None:

                for c in a:
                    if c is not None:
                        if c["max_temperature"] != '':
                            high_temp_data.append(int(c["max_temperature"]))

                        if c["min_temperature"] != '':
                            low_temp_data.append(int(c["min_temperature"]))

                        if c["mean_humidity"] != '':
                            mean_humidity_data.append(int(c["mean_humidity"]))

        avg_high_temp = int(sum(high_temp_data) / high_temp_data.__len__()) if high_temp_data.__len__() else 0
        low_avg_temp = int(sum(low_temp_data) / low_temp_data.__len__()) if low_temp_data.__len__() else 0

        if mean_humidity_data.__len__():
            avg_mean_humidity = int(sum(mean_humidity_data) / mean_humidity_data.__len__())
        else:
            avg_mean_humidity = 0

        print('\nHighest Average: %sC' % avg_high_temp)
        print('Lowest Average: %sC' % low_avg_temp)
        print('Average Mean Humidity: %s%%' % avg_mean_humidity)

    def chart_horizontal(self, files_yearly_parameter):
        for a in files_yearly_parameter:
            if a is not None:

                for c in a:
                    if c is not None:

                        if c["max_temperature"] != '':
                            self.draw_chart_horizontal(c["max_temperature"], HIGH_TEMP_COLOR, c["pkt"])
                        else:
                            self.draw_chart_horizontal(0, HIGH_TEMP_COLOR, c["pkt"])

                        if c["min_temperature"] != '':
                            self.draw_chart_horizontal(c["min_temperature"], LOW_TEMP_COLOR, c["pkt"])
                        else:
                            self.draw_chart_horizontal(0, LOW_TEMP_COLOR, c["pkt"])

    def double_chart_horizontal(self, files_yearly_parameter):
        high_temp_data, low_temp_data = 0, 0
        for a in files_yearly_parameter:
            if a is not None:

                for c in a:
                    if c is not None:
                            high_temp_data = c["max_temperature"] if c["max_temperature"] != '' else 0
                            low_temp_data = c["min_temperature"] if c["min_temperature"] != '' else 0

                    self.draw_double_chart_horizontal(low_temp_data, high_temp_data, c["pkt"])
                    high_temp_data, low_temp_data = 0, 0

    def draw_chart_horizontal(self, count, color, date_value):
        count = int(count)
        print("\033[%d;10m%s " % (DEFAULT_COLOR, date_value[7:]), end='')

        for i in range(count):
            print("\033[%d;10m+" % int(color), end='')

        print("\033[%d;10m %sC" % (DEFAULT_COLOR, count))

    def draw_double_chart_horizontal(self, mincount, maxcount, date_value):
        mincount = int(mincount)
        maxcount = int(maxcount)

        print("\033[%d;10m%s " % (DEFAULT_COLOR, date_value[7:]), end='')
        for i in range(mincount):
            print("\033[%d;10m+" % LOW_TEMP_COLOR, end='')
        for b in range(maxcount):
            print("\033[%d;10m+" % HIGH_TEMP_COLOR, end='')

        print("\033[%d;10m %sC-%sC" % (DEFAULT_COLOR, mincount, maxcount))


# reading data from files
class ReadData:
    def read_file_data(self, path):
        file = open(path, "r")
        csvreader = csv.reader(file)
        header = next(csvreader)

        datevalue_index = 0
        maxtemp_index = header.index("Max TemperatureC")
        mintemp_index = header.index("Min TemperatureC")
        maxhumid_index = header.index("Max Humidity")
        meanhumid_index = header.index(" Mean Humidity")

        requested_file_data = []
        # Loop through the lines in the file and get each coordinate
        for row in csvreader:
            weather_data = {}
            weather_data["pkt"] = row[datevalue_index]
            weather_data["max_temperature"] = row[maxtemp_index]
            weather_data["min_temperature"] = row[mintemp_index]
            weather_data["max_humidity"] = row[maxhumid_index]
            weather_data["mean_humidity"] = row[meanhumid_index]

            requested_file_data.append(weather_data)

        return requested_file_data

    def read_files(self, year, month, path):
        read_requested_data = glob.glob('%s/*%s*%s**.txt' % (path, year, month))
        read_files_data = []
        for file in read_requested_data:
            read_files_data.append(self.read_file_data(file))

        return read_files_data


# creating the reports given the results data structure.
class Reports:
    # Calculates high temp & day, low temp and day
    # and most humidity and day
    def fetch_high_low_temp_humidity_day(self, year, path):
        read_data_object = ReadData()
        files_yearly = read_data_object.read_files(year, "", path)

        hightemp = ComputingSubTaskResults()
        hightemp.high_low_temp_and_day(files_yearly)

    # Calculates avg high temp, avg low temp
    # and avg mean humidity
    def fetch_avg(self, year, month, path):
        read_data_object = ReadData()
        files_yearly = read_data_object.read_files(year, month, path)

        hightemp = ComputingSubTaskResults()
        hightemp.avg_high_temp(files_yearly)

    # 3. for month draw horizontal bar charts on the console for the highest and lowest temperature on each day.
    # Highest in red and lowest in blue.
    def draw_high_low_charts(self, year, month, path):
        read_data_object = ReadData()
        files_yearly = read_data_object.read_files(year, month, path)

        hightemp = ComputingSubTaskResults()
        hightemp.chart_horizontal(files_yearly)
        hightemp.double_chart_horizontal(files_yearly)


if __name__ == "__main__":
    def validate_input(to_validate):
        try:
            if len(to_validate) == 4:
                found = re.match("(20[0-1][0-9])", to_validate)
            else:
                found = re.match("(20[0-1][0-9])[//](1[0-2]|0[1-9]|\d)", to_validate)

            to_check_year = to_validate.split("/")
            if found is not None:
                if len(to_check_year[0]) == 4:
                    if (int(to_check_year[0]) > 2003) and (int(to_check_year[0]) < 2017):
                        return to_validate
                    else:
                        print("\nNo file exist against %s year!" % to_check_year[0])
                else:
                    print("Year is not in correct format(2006)!" % to_check_year[0])
            else:
                print("Format not correct!")
                return "0"

        except AttributeError:
            pass

    def check_file_path(path):
            return path if os.path.isdir(path) else print("Incorrect Path!")

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('path', type=check_file_path)
        parser.add_argument('-e', '--e', type=validate_input,
                            help='Enter Year YYYY!', default=None)
        parser.add_argument('-a', '--a', type=validate_input,
                            help='Enter Year YYYY/MM', default=None)
        parser.add_argument('-c', '--c', type=validate_input,
                            help='Enter Year YYYY/MM', default=None)

        args = parser.parse_args()
        compute_result = ComputingSubTaskResults()

        if args.e is not None:
            if len(args.e) == 4:
                compute_result.sub_task_1(args.e, args.path)
            elif len(args.e) < 4 or len(args.e) > 4:
                print("\nPlease follow -e yyyy format!")

        if args.a is not None:
            if len(args.a) in [6, 7]:
                compute_result.sub_task_2(args.a, args.path)
            elif len(args.a) <= 5:
                print("\nPlease follow -a yyyy/m or yyyy/mm format!")

        if args.c is not None:
            if len(args.c) > 5:
                compute_result.sub_task_3(args.c, args.path)
            elif len(args.c) <= 5:
                print("\nPlease follow -c yyyy/m or yyyy/mm format!")

        if args.e is None and args.a is None and args.c is None:
            print("Try Again!")

    except TypeError:
        print(TypeError)
