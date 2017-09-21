import os
import csv
import glob
import enum

import argparse
import datetime

from dateutil import parser


class ReportType(enum.Enum):
    YEAR, YEAR_MONTH, BAR_CHART = range(1,4)


class WeatherModel:

    def __init__(self, reading_line):
        self.date = reading_line.get("PKT", reading_line.get("PKST"))
        self.max_temp = float(reading_line["Max TemperatureC"])
        self.min_temp = float(reading_line["Min TemperatureC"])
        self.max_humidity = float(reading_line["Max Humidity"])
        self.mean_humidity = float(reading_line["Mean Humidity"])


class WeatherMan:

    BLACK = "\033[1;30m"
    BLUE = "\033[1;34m"
    PINK = "\033[1;35m"
    RED = "\033[1;31m"

    def __init__(self):
        self.weather_yearly_readings = []
        self.weather_monthly_readings = []

    def validate_path(self, path):
        if os.path.isdir(path):
            return path

    def month_to_month_name(self, month):
        current_date = datetime.datetime.now()
        month = current_date.replace(month=month).strftime("%b")
        return month

    def read_monthly_files(self, path, year_month):
        year, month = year_month.split('/')
        month = self.month_to_month_name(int(month))
        return self.read_weather_files(path, str(year), month)

    def read_weather_files(self, path, year, month="*"):
        file_paths = []
        file_path = path + "/*" + year + "_" + month + ".txt"
        for file_path_ in glob.glob(file_path):
            file_paths.append(file_path_)
        return file_paths

    def read_monthly_readings_from_saved_readings(self, readings, year, month):
        monthly_readings = []
        for reading in readings:
            if year + "-" + month + "-" in reading.date:
                monthly_readings.append(reading)
        return monthly_readings

    def read_weather_values(self, line, weather_readings):
        if line["Max TemperatureC"] and line["Min TemperatureC"] and line["Max Humidity"] and line["Mean Humidity"]:
            weather = WeatherModel(line)
            weather_readings.append(weather)

    def read_weather_file_readings(self, weather_file, weather_readings):
        with open(weather_file, 'r') as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            for line in reader:
                self.read_weather_values(line,weather_readings)

    def populate_weather_readings(self, weather_files):
        weather_readings = []
        for weather_file in weather_files:
            self.read_weather_file_readings(weather_file, weather_readings)
        return weather_readings

    def calculate_highest_temperature(self, readings):
        high_temp_reading = max(readings, key=lambda x: x.max_temp)
        return high_temp_reading

    def calculate_lowest_temperature(self, readings):
        low_temp_reading = min(readings, key=lambda x: x.min_temp)
        return low_temp_reading

    def calculate_highest_humidity(self, readings):
        high_humid_reading = max(readings, key=lambda x: x.max_humidity)
        return high_humid_reading

    def calculate_average_high_temp(self, readings):
        temp_sum = sum(c.max_temp for c in readings)
        temp_length = len(readings)
        avg_temp = round(temp_sum / temp_length)
        return avg_temp

    def calculate_average_low_temp(self, readings):
        temp_sum = sum(c.min_temp for c in readings)
        temp_length = len(readings)
        avg_temp = round(temp_sum / temp_length)
        return avg_temp

    def calculate_average_mean_humidity(self, readings):
        humid_sum = sum(c.mean_humidity for c in readings)
        humid_length = len(readings)
        avg_humid = round(humid_sum / humid_length)
        return avg_humid

    def compute_result(self, weather_readings, result_type):

        results = {}

        if result_type == ReportType.YEAR:
            results["Highest"] = self.calculate_highest_temperature(weather_readings)
            results["Humidity"] = self.calculate_highest_humidity(weather_readings)
            results["Lowest"] = self.calculate_lowest_temperature(weather_readings)

        elif result_type == ReportType.YEAR_MONTH:
            results["Highest Average"] = self.calculate_average_high_temp(weather_readings)
            results["Lowest Average"] = self.calculate_average_low_temp(weather_readings)
            results["Average Mean Humidity"] = self.calculate_average_mean_humidity(weather_readings)

        else:
            results = weather_readings

        return results

    def draw_chart(self, temperature_readings):

        for temperature in temperature_readings:

            day = parser.parse(temperature.date).strftime("%d")

            high_temp_point = round(abs(temperature.max_temp))
            high_temp_value = str(round(temperature.max_temp))

            low_temp_point = round(abs(temperature.min_temp))
            low_temp_value = str(round(temperature.min_temp))

            high_temp_line = self.RED + "" + "+" * high_temp_point
            low_temp_line = self.BLUE + "" + "+" * low_temp_point

            print(self.PINK + day + " " + low_temp_line + high_temp_line + " "
                  + self.PINK + low_temp_value + "C" + "-" + high_temp_value + "C")

    def populate_year_report(self, weather_man_results):

        max_temp = weather_man_results["Highest"]
        min_temp = weather_man_results["Lowest"]
        max_humid = weather_man_results["Humidity"]

        print("Highest: "+str(max_temp.max_temp)+"C on "+ parser.parse(max_temp.date).strftime("%b %d"))
        print("Lowest: " + str(min_temp.min_temp) + "C on " + parser.parse(min_temp.date).strftime("%b %d"))
        print("Humidity: " + str(max_humid.max_humidity) + "% on " + parser.parse(max_humid.date).strftime("%b %d"))

    def populate_year_month_report(self, weather_man_results):
        avg_highest_temp = weather_man_results["Highest Average"]
        avg_lowest_temp = weather_man_results["Lowest Average"]
        avg_mean_humid = weather_man_results["Average Mean Humidity"]

        print("Highest Average: "+str(avg_highest_temp)+"C")
        print("Lowest Average: " + str(avg_lowest_temp) + "C")
        print("Average Mean Humidity: " + str(avg_mean_humid) + "%")

    def populate_bar_chart_report(self, temperature_readings, year, month):

        print(month + " " + year)

        self.draw_chart(temperature_readings)

    def generate_report(self, weather_man_results, report_type, year="", month=""):

        if report_type == ReportType.BAR_CHART:
            print("\n\n")
            self.populate_bar_chart_report(weather_man_results, year, month)
        elif report_type == ReportType.YEAR_MONTH:
            print("\n\n")
            self.populate_year_month_report(weather_man_results)
        else:
            print("\n\n")
            self.populate_year_report(weather_man_results)

    def yearly_weather_report(self, path, year):

        reading_files = self.read_weather_files(path, str(year))
        if reading_files:
            readings = self.populate_weather_readings(reading_files)
            weather_results = self.compute_result(readings, ReportType.YEAR)
            self.generate_report(weather_results, ReportType.YEAR)
            self.weather_yearly_readings = readings
        else:
            print("Yearly weather readings not exist")

    def monthly_weather_report(self, path, year_month):
        readings = []
        reading_files = []
        year, month = year_month.split('/')

        check_saved_year = any(year in x.date for x in self.weather_yearly_readings)
        if check_saved_year:
            readings = self.read_monthly_readings_from_saved_readings(self.weather_yearly_readings, year, str(int(month)))
        else:
            reading_files = self.read_monthly_files(path, year_month)
        if reading_files or readings:
            if reading_files:
                readings = self.populate_weather_readings(reading_files)
            weather_results = self.compute_result(readings, ReportType.YEAR_MONTH)
            self.generate_report(weather_results, ReportType.YEAR_MONTH)
            self.weather_monthly_readings = readings
        else:
            print("Weather readings not exist")

    def chart_weather_report(self, path, year_month):
        readings = []
        reading_files = []
        year, month = year_month.split('/')
        month = str(int(month))

        check_saved_month_from_monthly_readings = any(month in x.date for x in self.weather_monthly_readings )
        if check_saved_month_from_monthly_readings:
            readings = self.weather_monthly_readings
        else:
            check_saved_month_from_yearly_readings = any(month in x.date for x in self.weather_yearly_readings)
            if check_saved_month_from_yearly_readings:
                readings = self.read_monthly_readings_from_saved_readings(self.weather_yearly_readings, year, month)
            else:
                reading_files = self.read_monthly_files(path, year_month)
        if reading_files or readings:

            if reading_files:
                readings = self.populate_weather_readings(reading_files)

            weather_results = self.compute_result(readings, ReportType.BAR_CHART)

            month = self.month_to_month_name(int(month))
            self.generate_report(weather_results, ReportType.BAR_CHART, year, month)

            self.weather_monthly_readings = readings
        else:
            print("Weather readings not exist")


weatherman = WeatherMan()
arg_parser = argparse.ArgumentParser(description='Weatherman data analysis')
arg_parser.add_argument('path', type=weatherman.validate_path, help='Enter weather files directory path')
arg_parser.add_argument('-c', type=str, default=None,
                        help='(usage: -c yyyy/mm) To see two horizontal bar charts on the console'
                             ' for the highest and lowest temperature on each day.')
arg_parser.add_argument('-e', type=int, default=None,
                        help='(usage: -e yyyy) To see highest temperature and day,'
                             ' lowest temperature and day, most humid day and humidity')
arg_parser.add_argument('-a', type=str, default=None,
                        help='(usage: -a yyyy/m) To see average highest temperature,'
                             ' average lowest temperature, average mean humidity.')
input_ = arg_parser.parse_args()
if input_.e:
    weatherman.yearly_weather_report(input_.path, input_.e)
if input_.a:
    weatherman.monthly_weather_report(input_.path, input_.a)
if input_.c:
    weatherman.chart_weather_report(input_.path, input_.c)
