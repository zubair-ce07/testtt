# weather_man_task
from datetime import datetime
import glob
import re
import argparse
import csv
import os

# constants
HIGH_TEMP_COLOR = 31    # RED
LOW_TEMP_COLOR = 34     # BLUE
DEFAULT_COLOR = 37      # DEFAULT


# class for computing the calculations given the readings data structure.
class ComputeResults:
    def __init__(self):
        self.max_temp_data, self.low_temp_data = [], []
        self.max_humid_data, self.mean_humid_data = [], []

    def temp_result(self, files_yearly_param):
        date_data = {}

        for read_dict in files_yearly_param:
            if read_dict:

                for sub_dict in read_dict:
                    if sub_dict:
                        if sub_dict["max_temperature"] != '':
                            self.max_temp_data.append(int(sub_dict["max_temperature"]))
                            date_data[sub_dict["max_temperature"]] = sub_dict["pkt"]

                        if sub_dict["min_temperature"] != '':
                            self.low_temp_data.append(int(sub_dict["min_temperature"]))
                            date_data[sub_dict["min_temperature"]] = sub_dict["pkt"]

                        if sub_dict["max_humidity"] != '':
                            self.max_humid_data.append(int(sub_dict["max_humidity"]))
                            date_data[sub_dict["max_humidity"]] = sub_dict["pkt"]

        max_temp = max(self.max_temp_data) if self.max_temp_data else 0
        min_temp = min(self.low_temp_data) if self.low_temp_data else 0
        max_humid = max(self.max_humid_data) if self.max_humid_data else 0

        high_date_converted = datetime.strptime(date_data.get(str(max_temp)), '%Y-%m-%d')
        low_date_converted = datetime.strptime(date_data.get(str(min_temp)), '%Y-%m-%d')
        humid_date_converted = datetime.strptime(date_data.get(str(max_humid)), '%Y-%m-%d')

        print('\nHighest: {}C on {} {}'.format(max_temp, high_date_converted.strftime("%B"),
                                               high_date_converted.day))
        print('Lowest: {}C on {} {}'.format(min_temp, low_date_converted.strftime("%B"),
                                            low_date_converted.day))
        print('Humidity: {}% on {} {}'.format(max_humid, humid_date_converted.strftime("%B"),
                                              humid_date_converted.day))
        self.max_temp_data[:], self.low_temp_data[:], self.max_humid_data[:] = [], [], []

    def avg_temp_result(self, monthly_file_param):
        for read_dict in monthly_file_param:
            if read_dict:

                for sub_dict in read_dict:
                    if sub_dict:
                        if sub_dict["max_temperature"] != '':
                            self.max_temp_data.append(int(sub_dict["max_temperature"]))

                        if sub_dict["min_temperature"] != '':
                            self.low_temp_data.append(int(sub_dict["min_temperature"]))

                        if sub_dict["mean_humidity"] != '':
                            self.mean_humid_data.append(int(sub_dict["mean_humidity"]))

        avg_high_temp = int(sum(self.max_temp_data) / len(self.max_temp_data)) if self.max_temp_data else 0
        low_avg_temp = int(sum(self.low_temp_data) / len(self.low_temp_data)) if self.low_temp_data else 0
        avg_mean_humidity = int(sum(self.mean_humid_data) / len(self.mean_humid_data)) if self.mean_humid_data else 0

        print('\nHighest Average: {}C'.format(avg_high_temp))
        print('Lowest Average: {}C'.format(low_avg_temp))
        print('Average Mean Humidity: {}%'.format(avg_mean_humidity))

        self.max_temp_data[:], self.low_temp_data[:], self.mean_humid_data[:] = [], [], []

    def single_line_chart(self, monthly_file_param):
        for read_dict in monthly_file_param:
            if read_dict:

                for sub_dict in read_dict:
                    if sub_dict:

                        if sub_dict["max_temperature"] != '':
                            self.draw_single_chart(int(sub_dict["max_temperature"]), HIGH_TEMP_COLOR, sub_dict["pkt"])
                        else:
                            self.draw_single_chart(0, HIGH_TEMP_COLOR, sub_dict["pkt"])

                        if sub_dict["min_temperature"] != '':
                            self.draw_single_chart(int(sub_dict["min_temperature"]), LOW_TEMP_COLOR, sub_dict["pkt"])
                        else:
                            self.draw_single_chart(0, LOW_TEMP_COLOR, sub_dict["pkt"])

    def double_line_chart(self, monthly_file_param):
        max_temp_data, low_temp_data = 0, 0
        for read_dict in monthly_file_param:
            if read_dict:

                for sub_dict in read_dict:
                    if sub_dict:
                        max_temp_data = sub_dict["max_temperature"] if sub_dict["max_temperature"] != '' else 0
                        low_temp_data = sub_dict["min_temperature"] if sub_dict["min_temperature"] != '' else 0

                    self.draw_double_chart(int(low_temp_data), int(max_temp_data), sub_dict["pkt"])
                    high_temp_data, low_temp_data = 0, 0

    def draw_single_chart(self, count, color, date_value):
        print("\033[{};10m{} ".format(DEFAULT_COLOR, date_value[7:]), end='')

        for i in range(count):
            print("\033[{};10m+".format(int(color)), end='')

        print("\033[{};10m {}C".format(DEFAULT_COLOR, count))

    def draw_double_chart(self, min_range, max_range, date_value):
        print("\033[{};10m{} ".format(DEFAULT_COLOR, date_value[7:]), end='')
        for i in range(min_range):
            print("\033[{};10m+".format(LOW_TEMP_COLOR), end='')
        for b in range(max_range):
            print("\033[{};10m+".format(HIGH_TEMP_COLOR), end='')

        print("\033[{};10m {}C-{}C".format(DEFAULT_COLOR, min_range, max_range))


# reading data from files
class ReadData:
    def read_file_data(self, path):
        read_file = open(path, "r")
        csv_reader = csv.reader(read_file)
        header = next(csv_reader)

        date_index = 0
        max_temp_index = header.index("Max TemperatureC")
        min_temp_index = header.index("Min TemperatureC")
        max_humid_index = header.index("Max Humidity")
        mean_humid_index = header.index(" Mean Humidity")

        requested_file_data = []

        # Loop through the lines in the file and get each coordinate
        for row in csv_reader:
            weather_data = {}
            weather_data["pkt"] = row[date_index]
            weather_data["max_temperature"] = row[max_temp_index]
            weather_data["min_temperature"] = row[min_temp_index]
            weather_data["max_humidity"] = row[max_humid_index]
            weather_data["mean_humidity"] = row[mean_humid_index]

            requested_file_data.append(weather_data)

        return requested_file_data

    def read_files(self, year, month, path):
        read_requested_data = glob.glob('{}/*{}*{}**.txt'.format(path, year, month))
        read_files_data = []
        for file in read_requested_data:
            read_files_data.append(self.read_file_data(file))

        return read_files_data


# creating the reports given the results data structure.
class Reports:
    def __init__(self):
        self.read_data_object = ReadData()
        self.compute_result = ComputeResults()

    # Calculates high temp & day, low temp and day
    # and most humidity and day
    def sub_task_1(self, year, path):
        yearly_files = self.read_data_object.read_files(year, "", path)
        self.compute_result.temp_result(yearly_files)

    # Calculates avg high temp, avg low temp
    # and avg mean humidity
    def sub_task_2(self, year_month_value, path):
        month_value = year_month_value
        month_value_split = month_value.split("/")
        date_converted = datetime.strptime(month_value_split[1], '%m')

        monthly_file = self.read_data_object.read_files(month_value_split[0], date_converted.strftime("%b"), path)
        self.compute_result.avg_temp_result(monthly_file)

    # 3. for month draw horizontal bar charts on the console for the highest and lowest temperature on each day.
    # Highest in red and lowest in blue.
    def sub_task_3(self, year_month_value, path):
        month_value = year_month_value
        month_value_split = month_value.split("/")
        date_converted = datetime.strptime(month_value_split[1], '%m')

        print("\n{} {}".format(date_converted.strftime("%B"), month_value_split[0]))

        monthly_file = self.read_data_object.read_files(month_value_split[0], date_converted.strftime("%b"), path)
        self.compute_result.single_line_chart(monthly_file)
        self.compute_result.double_line_chart(monthly_file)


# Main
if __name__ == "__main__":
    def validate_input(to_validate):
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
                    print("\nNo file exist against {} year!".format(to_check_year[0]))
            else:
                print("Year is not in correct format({})!".format(to_check_year[0]))
        else:
            print("Format not correct! {}".format(to_validate))
            return "0"

    def check_file_path(path):
        if os.path.isdir(path) and glob.glob('{}/*.txt'.format(path)):
            return path
        else:
            print("incorrect path or no files on mentioned path!\n {}".format(path))
            return False

    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=check_file_path)
    parser.add_argument('-e', '--e', type=validate_input,
                        help='Enter Year YYYY!', default=None)
    parser.add_argument('-a', '--a', type=validate_input,
                        help='Enter Year YYYY/MM', default=None)
    parser.add_argument('-c', '--c', type=validate_input,
                        help='Enter Year YYYY/MM', default=None)

    args = parser.parse_args()
    if args.path:
        read_reports = Reports()

        if args.e:
            if len(args.e) == 4:
                read_reports.sub_task_1(args.e, args.path)
            elif len(args.e) < 4 or len(args.e) > 4:
                print("\nPlease follow -e yyyy format!")

        if args.a:
            if len(args.a) in [6, 7]:
                read_reports.sub_task_2(args.a, args.path)
            elif len(args.a) <= 5 or len(args.a) > 7:
                print("\nPlease follow -a yyyy/m or yyyy/mm format!")

        if args.c:
            if len(args.c) <= 5:
                print("\nPlease follow -c yyyy/m or yyyy/mm format!")
            else:
                read_reports.sub_task_3(args.c, args.path)

        if args.e is None and args.a is None and args.c is None:
            print("Try Again!")
