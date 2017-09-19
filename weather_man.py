import os
import glob

import argparse
import datetime

from weather_man_helper import ReportType
from weather_man_helper import WeatherManFileParser
from weather_man_helper import WeatherManResultCalculator
from weather_man_helper import WeatherManReportGenerator


class WeatherMan:

    def __init__(self):
        self.__weather_yearly_readings = list()
        self.__weather_monthly_readings = list()

    def validate_path(self, path):
        is_directory_exist = os.path.isdir(path)
        if is_directory_exist:
            return path
        else:
            return False

    def month_to_month_name(self, month):
        current_date = datetime.datetime.now()
        month = current_date.replace(month=month).strftime("%b")
        return month

    def read_monthly_files(self, path, year_month):
        year = year_month.split('/')[0]
        month = year_month.split('/')[1]
        month = self.month_to_month_name(int(month))
        return self.weather_files(path, str(year), month)

    def weather_files(self, path, year, month="*"):
        file_paths = list()
        file_path = path + "/*" + year + "_" + month + ".txt"
        for file_path_ in glob.glob(file_path):
            file_paths.append(file_path_)
        return file_paths

    def read_yearly_readings(self, reading_files):
        file_parser = WeatherManFileParser()
        return file_parser.populate_weather_readings(reading_files)

    def read_monthly_readings(self, readings, year, month):
        monthly_readings = list()
        for reading in readings:
            if year + "-" + month + "-" in reading.date:
                monthly_readings.append(reading)
        return monthly_readings

    def weather_chart_report(self, readings_report_generator, year_month, weather_results, report_type):
        year = year_month.split('/')[0]
        month = year_month.split('/')[1]
        month = self.month_to_month_name(int(month))
        readings_report_generator.generate_report(weather_results, report_type, year, month)

    def weather_man_report(self, path, year_month, report_type):

        readings = list()
        reading_files = list()

        if self.__weather_yearly_readings:
            readings = self.__weather_yearly_readings
        else:
            if isinstance(year_month, int):
                reading_files = self.weather_files(path, str(year_month))
            else:
                reading_files = self.read_monthly_files(path,year_month)

        if self.__weather_monthly_readings:
            readings = self.__weather_monthly_readings

        if reading_files or readings:

            if reading_files:
                readings = self.read_yearly_readings(reading_files)

            if not report_type == ReportType.YEAR and not self.__weather_monthly_readings and self.__weather_yearly_readings:
                year = (year_month.split('/')[0])
                month = str(int(year_month.split('/')[1]))
                readings = self.read_monthly_readings(readings, year, month)

            if report_type == ReportType.YEAR:
                self.__weather_yearly_readings = readings
            else:
                self.__weather_monthly_readings = readings

            readings_calculator = WeatherManResultCalculator()
            weather_results = readings_calculator.compute_result(readings, report_type)

            readings_report_generator = WeatherManReportGenerator()
            if report_type == ReportType.TWO_BAR_CHART:
                self.weather_chart_report(readings_report_generator, year_month, weather_results, report_type)
            else:
                readings_report_generator.generate_report(weather_results, report_type)
        else:
            print("Weather readings not exist")

    def __del__(self):
        self.__weather_yearly_readings.clear()
        self.__weather_monthly_readings.clear()


weatherman = WeatherMan()

parser = argparse.ArgumentParser(description='Weatherman data analysis')

parser.add_argument('path', type=weatherman.validate_path, help='Enter weather files directory path')

parser.add_argument('-c', type=str, default=None,
                    help='(usage: -c yyyy/mm) To see two horizontal bar charts on the console'
                         ' for the highest and lowest temperature on each day.')

parser.add_argument('-e', type=int, default=None,
                    help='(usage: -e yyyy) To see highest temperature and day,'
                         ' lowest temperature and day, most humid day and humidity')

parser.add_argument('-a', type=str, default=None,
                    help='(usage: -a yyyy/m) To see average highest temperature,'
                         ' average lowest temperature, average mean humidity.')

input_ = parser.parse_args()

if input_.e:
    weatherman.weather_man_report(input_.path, input_.e, ReportType.YEAR)
if input_.a:
    weatherman.weather_man_report(input_.path, input_.a, ReportType.YEAR_MONTH)
if input_.c:
    weatherman.weather_man_report(input_.path, input_.c, ReportType.TWO_BAR_CHART)

