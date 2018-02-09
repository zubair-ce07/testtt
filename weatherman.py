from datetime import datetime
import glob
import re
import argparse
import csv
import os

HIGH_TEMP_COLOR = 31    # RED
LOW_TEMP_COLOR = 34     # BLUE
DEFAULT_COLOR = 37      # DEFAULT


class Weather:
    def __init__(self):
        self.pkt = "1900-01-01"
        self.max_temperature = 0
        self.min_temperature = 0
        self.max_humidity = 0
        self.mean_humidity = 0


class ResultHolder:
    def __init__(self):
        self.max_temperature = 0
        self.max_temperature_date = "1900-01-01"
        self.min_temperature = 0
        self.min_temperature_date = "1900-01-01"
        self.max_humidity = 0
        self.max_humidity_date = "1900-01-01"
        self.avg_high_temperature = 0
        self.avg_low_temperature = 0
        self.avg_mean_humidity = 0


class ResultViewer:
    def __init__(self):
        self.max_temp, self.low_temp = [], []
        self.max_humid, self.mean_humid = [], []
        self.result_value = ResultHolder()

    def display_relative_temp_and_humidity(self, files_yearly_param):
        pkt_date = {}
        for read_dict in files_yearly_param:
            for sub_dict in read_dict:
                if sub_dict.max_temperature:
                    self.max_temp.append(int(sub_dict.max_temperature))
                    pkt_date[sub_dict.max_temperature] = sub_dict.pkt

                if sub_dict.min_temperature:
                    self.low_temp.append(int(sub_dict.min_temperature))
                    pkt_date[sub_dict.min_temperature] = sub_dict.pkt

                if sub_dict.max_humidity:
                    self.max_humid.append(int(sub_dict.max_humidity))
                    pkt_date[sub_dict.max_humidity] = sub_dict.pkt

        self.result_value.max_temperature = max(self.max_temp) if self.max_temp else 0
        self.result_value.min_temperature = min(self.low_temp) if self.low_temp else 0
        self.result_value.max_humidity = max(self.max_humid) if self.max_humid else 0

        self.result_value.max_temperature_date = pkt_date.get(str(self.result_value.max_temperature))
        self.result_value.min_temperature_date = pkt_date.get(str(self.result_value.min_temperature))
        self.result_value.max_humidity_date = pkt_date.get(str(self.result_value.max_humidity))

        self.print_temp_and_humid(self.result_value)
        self.max_temp, self.low_temp, self.max_humid = [], [], []

    def print_temp_and_humid(self, result):
        print('\nHighest: {}C on {} {}'.format(result.max_temperature,
                                               result.max_temperature_date.strftime("%B"),
                                               result.max_temperature_date.day))
        print('Lowest: {}C on {} {}'.format(result.min_temperature,
                                            result.min_temperature_date.strftime("%B"),
                                            result.min_temperature_date.day))
        print('Humidity: {}% on {} {}'.format(result.max_humidity,
                                              result.max_humidity_date.strftime("%B"),
                                              result.max_humidity_date.day))

    def display_avg_relative_temp_and_humidity(self, monthly_file_param):
        for read_dict in monthly_file_param:
            for sub_dict in read_dict:
                if sub_dict.max_temperature:
                    self.max_temp.append(int(sub_dict.max_temperature))

                if sub_dict.min_temperature:
                    self.low_temp.append(int(sub_dict.min_temperature))

                if sub_dict.mean_humidity:
                    self.mean_humid.append(int(sub_dict.mean_humidity))

        self.result_value.avg_high_temperature = int(sum(self.max_temp) / len(self.max_temp)) if self.max_temp else 0
        self.result_value.avg_low_temperature = int(sum(self.low_temp) / len(self.low_temp)) if self.low_temp else 0
        self.result_value.avg_mean_humidity = int(sum(self.mean_humid) / len(self.mean_humid)) if self.mean_humid else 0

        self.print_avg_temp_and_humid(self.result_value)
        self.max_temp, self.low_temp, self.mean_humid = [], [], []

    def print_avg_temp_and_humid(self, result):
        print('\nHighest Average: {}C'.format(result.avg_high_temperature))
        print('Lowest Average: {}C'.format(result.avg_low_temperature))
        print('Average Mean Humidity: {}%'.format(result.avg_mean_humidity))

    def display_single_line_chart(self, monthly_file_param):
        for read_dict in monthly_file_param:
            for sub_dict in read_dict:
                if sub_dict.max_temperature:
                    self.print_single_chart(int(sub_dict.max_temperature), HIGH_TEMP_COLOR,
                                            str(sub_dict.pkt))
                else:
                    self.print_single_chart(0, HIGH_TEMP_COLOR, str(sub_dict.pkt))

                if sub_dict.min_temperature:
                    self.print_single_chart(int(sub_dict.min_temperature), LOW_TEMP_COLOR,
                                            str(sub_dict.pkt))
                else:
                    self.print_single_chart(0, LOW_TEMP_COLOR, str(sub_dict.pkt))

    def display_double_line_chart(self, monthly_file_param):
        for read_dict in monthly_file_param:
            for sub_dict in read_dict:
                max_temp = sub_dict.max_temperature if sub_dict.max_temperature else 0
                low_temp = sub_dict.min_temperature if sub_dict.min_temperature else 0

                self.print_double_chart(int(low_temp), int(max_temp), str(sub_dict.pkt))

    def print_single_chart(self, count, color, month_date):
        print("\033[{};10m{} ".format(DEFAULT_COLOR, month_date[8:10]), end='')

        for _ in range(count):
            print("\033[{};10m+".format(int(color)), end='')

        print("\033[{};10m {}C".format(DEFAULT_COLOR, count))

    def print_double_chart(self, min_range, max_range, month_date):
        print("\033[{};10m{} ".format(DEFAULT_COLOR, month_date[8:10]), end='')
        for _ in range(min_range):
            print("\033[{};10m+".format(LOW_TEMP_COLOR), end='')
        for _ in range(max_range):
            print("\033[{};10m+".format(HIGH_TEMP_COLOR), end='')

        print("\033[{};10m {}C-{}C".format(DEFAULT_COLOR, min_range, max_range))


class FileReader:
    def read_file(self, file_path):
        read_file_input = open(file_path, "r")
        csv_reader = csv.reader(read_file_input)
        header = next(csv_reader)

        date_index = 0
        max_temp_index = header.index("Max TemperatureC")
        min_temp_index = header.index("Min TemperatureC")
        max_humid_index = header.index("Max Humidity")
        mean_humid_index = header.index(" Mean Humidity")

        requested_file = []

        # Loop through the lines in the file and get each coordinate
        for row in csv_reader:
            weather_reading = Weather()
            weather_reading.pkt = datetime.strptime(row[date_index], '%Y-%m-%d')
            weather_reading.max_temperature = row[max_temp_index]
            weather_reading.min_temperature = row[min_temp_index]
            weather_reading.max_humidity = row[max_humid_index]
            weather_reading.mean_humidity = row[mean_humid_index]

            requested_file.append(weather_reading)

        return requested_file

    def read_files(self, year, month, file_path):
        requested_files = glob.glob('{}/*{}*{}**.txt'.format(file_path, year, month))
        file_values = []
        for file in requested_files:
            file_values.append(self.read_file(file))

        return file_values


class Reports:
    def __init__(self):
        self.read_file_object = FileReader()
        self.view_result = ResultViewer()

    # shows high, low temp and max humidity and day
    def yearly_report(self, year, path):
        yearly_files = self.read_file_object.read_files(year, "", path)
        self.view_result.display_relative_temp_and_humidity(yearly_files)

    # shows average high, low temp and avg mean humidity
    def monthly_report(self, year_month, path):
        month_split = year_month.split("/")
        month_format = datetime.strptime(month_split[1], '%m')

        monthly_file = self.read_file_object.read_files(month_split[0], month_format.strftime("%b"), path)
        self.view_result.display_avg_relative_temp_and_humidity(monthly_file)

    # shows relative temperature chart
    def draw_monthly_chart(self, year_month, path):
        month_split = year_month.split("/")
        month_format = datetime.strptime(month_split[1], '%m')

        print("\n{} {}".format(month_format.strftime("%B"), month_split[0]))

        monthly_file = self.read_file_object.read_files(month_split[0], month_format.strftime("%b"), path)
        self.view_result.display_single_line_chart(monthly_file)
        self.view_result.display_double_line_chart(monthly_file)


if __name__ == "__main__":
    def validate_input(to_validate):
        to_check_year = to_validate.split("/")
        if len(to_validate) == 4:
            found = re.match("(20[0-1][0-9])", to_validate)
            if validate_input_year(to_check_year[0]) and found:
                return to_validate
            else:
                raise Exception("Format not correct! {}".format(to_validate))
        elif len(to_validate) in [6, 7]:
            found = re.match("(20[0-1][0-9])[//](1[0-2]|0[1-9]|\d)", to_validate)
            if validate_input_year(to_check_year[0]) and found:
                return to_validate
            else:
                raise Exception("Format not correct! {}".format(to_validate))
        else:
            raise Exception("Format not correct! {}".format(to_validate))

    def validate_input_year(year):
        if len(year) == 4:
            if (int(year) > 2003) and (int(year) < 2017):
                return year
            else:
                raise Exception("\nNo file exist against {} year!".format(year))
        else:
            raise Exception("Year is not in correct format({})!".format(year))

    def check_file_path(path):
        if os.path.isdir(path) and glob.glob('{}/*.txt'.format(path)):
            return path
        else:
            raise Exception("incorrect path or no files on mentioned path!\n {}".format(path))

    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=check_file_path)
    parser.add_argument('-e', '--e', type=validate_input,
                        help='Enter Year YYYY!', default=None)
    parser.add_argument('-a', '--a', type=validate_input,
                        help='Enter Year YYYY/MM', default=None)
    parser.add_argument('-c', '--c', type=validate_input,
                        help='Enter Year YYYY/MM', default=None)
    args = parser.parse_args()
    read_reports = Reports()

    if args.e:
        if len(args.e) == 4:
            read_reports.yearly_report(args.e, args.path)
        else:
            print("enter in -e yyyy format!")
    if args.a:
        if len(args.a) in [6, 7]:
            read_reports.monthly_report(args.a, args.path)
        else:
            print("enter in -a yyyy/mm or yyyy/m format!")
    if args.c:
        if len(args.c) in [6, 7]:
            read_reports.draw_monthly_chart(args.c, args.path)
        else:
            print("enter in -c yyyy/mm or yyyy/m format!")

    if args.e is None and args.a is None and args.c is None:
        print("Try Again!")
