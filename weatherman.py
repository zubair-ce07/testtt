from datetime import datetime
import glob
import re
import argparse
import csv
import os

HIGH_TEMP_COLOR = 31    # RED
LOW_TEMP_COLOR = 34     # BLUE
DEFAULT_COLOR = 37      # DEFAULT


class Validator:
    def validate_year(self, to_validate):
        if not datetime.strptime(to_validate, '%Y'):
            raise ValueError("Incorrect date format, should be YYYY")
        else:
            return to_validate

    def validate_year_month(self, to_validate):
        if not datetime.strptime(to_validate, '%Y/%m'):
            raise ValueError("Incorrect date format, should be YYYY/MM or YYYY/M")
        else:
            return to_validate

    def check_file_path(self, path):
        if os.path.isdir(path) and glob.glob('{}/*.txt'.format(path)):
            return path
        else:
            raise Exception("incorrect path or no files on mentioned path!\n {}".format(path))


class Weather:
    def __init__(self, pkt, max_temperature, min_temperature, max_humidity, mean_humidity):
        self.pkt = pkt
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity


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
        pkt_max_temp_date, pkt_min_temp_date, pkt_max_humid_date = {}, {}, {}
        for monthly_values in files_yearly_param:
            for per_day_values in monthly_values:
                    self.max_temp.append(per_day_values.max_temperature)
                    pkt_max_temp_date[per_day_values.max_temperature] = per_day_values.pkt

                    self.low_temp.append(per_day_values.min_temperature)
                    pkt_min_temp_date[per_day_values.min_temperature] = per_day_values.pkt

                    self.max_humid.append(per_day_values.max_humidity)
                    pkt_max_humid_date[per_day_values.max_humidity] = per_day_values.pkt

        self.result_value.max_temperature = max(self.max_temp)
        self.result_value.min_temperature = min(self.low_temp)
        self.result_value.max_humidity = max(self.max_humid)

        self.result_value.max_temperature_date = pkt_max_temp_date.get(self.result_value.max_temperature)
        self.result_value.min_temperature_date = pkt_min_temp_date.get(self.result_value.min_temperature)
        self.result_value.max_humidity_date = pkt_max_humid_date.get(self.result_value.max_humidity)
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
        for monthly_values in monthly_file_param:
            for per_day_values in monthly_values:
                    self.max_temp.append(per_day_values.max_temperature)
                    self.low_temp.append(per_day_values.min_temperature)
                    self.mean_humid.append(per_day_values.mean_humidity)

        self.result_value.avg_high_temperature = int(sum(self.max_temp) / len(self.max_temp))
        self.result_value.avg_low_temperature = int(sum(self.low_temp) / len(self.low_temp))
        self.result_value.avg_mean_humidity = int(sum(self.mean_humid) / len(self.mean_humid))

        self.print_avg_temp_and_humid(self.result_value)
        self.max_temp, self.low_temp, self.mean_humid = [], [], []

    def print_avg_temp_and_humid(self, result):
        print('\nHighest Average: {}C'.format(result.avg_high_temperature))
        print('Lowest Average: {}C'.format(result.avg_low_temperature))
        print('Average Mean Humidity: {}%'.format(result.avg_mean_humidity))

    def display_single_line_chart(self, monthly_file_param):
        for monthly_values in monthly_file_param:
            for per_day_values in monthly_values:
                    self.print_single_chart(per_day_values.max_temperature, HIGH_TEMP_COLOR,
                                            per_day_values.pkt)

                    self.print_single_chart(per_day_values.min_temperature, LOW_TEMP_COLOR,
                                            per_day_values.pkt)

    def display_double_line_chart(self, monthly_file_param):
        for monthly_values in monthly_file_param:
            for per_day_values in monthly_values:
                max_temp = per_day_values.max_temperature
                low_temp = per_day_values.min_temperature

                self.print_double_chart(low_temp, max_temp, per_day_values.pkt)

    def print_single_chart(self, count, color, month_date):
        print("\033[{};10m{} ".format(DEFAULT_COLOR, month_date.day), end='')

        for _ in range(count):
            print("\033[{};10m+".format(color), end='')

        print("\033[{};10m {}C".format(DEFAULT_COLOR, count))

    def print_double_chart(self, min_range, max_range, month_date):
        print("\033[{};10m{} ".format(DEFAULT_COLOR, month_date.day), end='')
        for _ in range(min_range):
            print("\033[{};10m+".format(LOW_TEMP_COLOR), end='')
        for _ in range(max_range):
            print("\033[{};10m+".format(HIGH_TEMP_COLOR), end='')

        print("\033[{};10m {}C-{}C".format(DEFAULT_COLOR, min_range, max_range))


class FileReader:
    def read_file(self, file_path):
        with open(file_path, "r") as file_content:
            csv.register_dialect('MyDialect', skipinitialspace=True)
            csv_reader = csv.DictReader(file_content, dialect='MyDialect')
            requested_file = []

            for row in csv_reader:
                pkt = row["PKT"] if 'PKT' in row.keys() else row["PKST"]
                max_temperature = row["Max TemperatureC"]
                min_temperature = row["Min TemperatureC"]
                max_humidity = row["Max Humidity"]
                mean_humidity = row["Mean Humidity"]

                if pkt and max_temperature and min_temperature and max_humidity and mean_humidity:
                    weather_reading = Weather(datetime.strptime(pkt, '%Y-%m-%d'), int(max_temperature),
                                              int(min_temperature), int(max_humidity), int(mean_humidity))
                    requested_file.append(weather_reading)

            return requested_file

    def read_files(self, year, month, file_path):
        requested_files = glob.glob('{}/*{}*{}**.txt'.format(file_path, year, month))
        file_values = []
        if requested_files:
            for file_to_read in requested_files:
                file_values.append(self.read_file(file_to_read))
            return file_values
        else:
            raise Exception("No files exist on mentioned path!")


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
    verify_input = Validator()
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=verify_input.check_file_path)
    parser.add_argument('-e', '--e', type=verify_input.validate_year,
                        help='Enter Year YYYY', default=None)
    parser.add_argument('-a', '--a', type=verify_input.validate_year_month,
                        help='Enter Year YYYY/MM', default=None)
    parser.add_argument('-c', '--c', type=verify_input.validate_year_month,
                        help='Enter Year YYYY/MM', default=None)
    args = parser.parse_args()
    read_reports = Reports()

    if not (args.e or args.a or args.c):
        raise Exception("Please Enter any argument!")

    if args.e:
        read_reports.yearly_report(args.e, args.path)
    if args.a:
        read_reports.monthly_report(args.a, args.path)
    if args.c:
        read_reports.draw_monthly_chart(args.c, args.path)
