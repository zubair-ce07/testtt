import sys
import csv
import logging
import operator
from dataclasses import dataclass

from constants import WEATHER_FILE_HEADERS
from constants import COLORS
from constants import TEMPERATURE_SYMBOL
from constants import CITY_NAME as CITY

from utils import helper
from utils.date_time_util import DateTimeUtil
from utils.file_util import FileUtil


@dataclass
class Stat:
    value: int
    date: str


@dataclass
class AvgStat:
    total: int
    count: int


class WeatherReport:
    def __init__(self, date_string, dir_path):
        self.files_path = dir_path
        self.date = date_string

    def path_builder(self, with_month=True):
        date_format = "%Y"
        short_month = '*'

        try:
            if with_month:
                date_format = "%Y/%m"
                short_month = DateTimeUtil.month_name(date_string=self.date)

            year = DateTimeUtil.parse_date(self.date, date_format).year
            return f"{self.files_path}/{CITY}_weather_{year}_{short_month}.txt"
        except ValueError as exp:
            logging.error(
                f"Error while parsing date: {str(exp)} date: {self.date}")
            sys.exit()

    @classmethod
    def read_date(cls, row):
        if WEATHER_FILE_HEADERS['Date'] in row:
            return row[WEATHER_FILE_HEADERS['Date']]

        return row[WEATHER_FILE_HEADERS['Date_S']]

    @classmethod
    def print_error(cls, exp, file_path):
        logging.error(
            f"Unexpected error while parsing file: {str(exp)} file: {file_path}"
        )

    @classmethod
    def print_bar_chart(cls, day, max_temperature, min_temperature):
        def print_temperature(day, color, temp):
            if helper.is_valid_int(temp):
                print(
                    f"{day.zfill(2)} {helper.colored_string(TEMPERATURE_SYMBOL, color, temp)} {temp}C"
                )

        def print_temperature_one_line(day, max_temperature_color,
                                       max_temperature, min_temperature_color,
                                       min_temperature):
            if (day and (max_temperature or min_temperature)):
                bar_str = [f"{day.zfill(2)} "]
                if max_temperature:
                    bar_str.append(
                        f"{helper.colored_string(TEMPERATURE_SYMBOL, max_temperature_color, max_temperature)}"
                    )
                if min_temperature:
                    bar_str.append(
                        f"{helper.colored_string(TEMPERATURE_SYMBOL, min_temperature_color, min_temperature)}"
                    )
                if max_temperature:
                    bar_str.append(f" {max_temperature}C")
                if min_temperature:
                    if max_temperature:
                        bar_str.append(' - ')
                    bar_str.append(f"{min_temperature}C")

                print(''.join(bar_str))

        print_temperature(day, COLORS['RED'], max_temperature)
        print_temperature(day, COLORS['BLUE'], min_temperature)
        print_temperature_one_line(day, COLORS['RED'], max_temperature,
                                   COLORS['BLUE'], min_temperature)

    def calc_month_min_max_stats(self):
        path = self.path_builder()
        file_names_list = FileUtil.file_names_list(path)
        if not file_names_list:
            return
        file_path = file_names_list[0]

        try:
            year = DateTimeUtil.parse_date(self.date).year
            full_month = DateTimeUtil.month_name(date_string=self.date,
                                                 short_name=False)

            with open(file_path, 'r') as file:
                # Skip empty line, if on start of file
                FileUtil.skip_blank_line(file)

                reader = csv.DictReader(file, delimiter=',')
                print(f"{full_month} {year}")

                for row in reader:
                    day = DateTimeUtil.parse_date(self.read_date(row),
                                                  "%Y-%m-%d").day
                    max_temperature = row[
                        WEATHER_FILE_HEADERS['MaxTemperatureC']]
                    min_temperature = row[
                        WEATHER_FILE_HEADERS['MinTemperatureC']]

                    if day:
                        self.print_bar_chart(str(day), max_temperature,
                                             min_temperature)

        except ValueError as exp:
            self.print_error(exp, file_path)
        except IOError as exp:
            self.print_error(exp, file_path)
            sys.exit()

    @classmethod
    def update_avg_stat(cls, actual, current):
        if helper.is_valid_int(current):
            actual.total += int(current)
            actual.count += 1

    def calc_month_avg_stats(self):
        try:
            path = self.path_builder()
            file_path = FileUtil.file_names_list(path)
            if not file_path:
                return

            highest_temp = AvgStat(0, 0)
            lowest_temp = AvgStat(0, 0)
            humidity = AvgStat(0, 0)

            file_path = file_path[0]
            with open(file_path, 'r') as file:
                # Skip empty line, if on start of file
                FileUtil.skip_blank_line(file)

                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    max_temperature = row[
                        WEATHER_FILE_HEADERS['MaxTemperatureC']]
                    min_temperature = row[
                        WEATHER_FILE_HEADERS['MinTemperatureC']]
                    humidity_val = row[WEATHER_FILE_HEADERS['MeanHumidity']]

                    self.update_avg_stat(highest_temp, max_temperature)
                    self.update_avg_stat(lowest_temp, min_temperature)
                    self.update_avg_stat(humidity, humidity_val)

            avg_highest_temp = helper.int_divison_util(highest_temp.total,
                                                       highest_temp.count)
            avg_lowest_temp = helper.int_divison_util(lowest_temp.total,
                                                      lowest_temp.count)
            avg_humidity = helper.int_divison_util(humidity.total,
                                                   humidity.count)

            print(f"Highest Average: {avg_highest_temp}C")
            print(f"Lowest Average: {avg_lowest_temp}C")
            print(f"Average Humidity: {avg_humidity}%")

        except ValueError as exp:
            self.print_error(exp, file_path)
        except IOError as exp:
            self.print_error(exp, file_path)
            sys.exit()

    @classmethod
    def print_year_stats(cls, weather_attr, msg, unit):
        if (helper.is_valid_int(weather_attr.value) and weather_attr.date):
            max_temperature_day = DateTimeUtil.parse_date(
                weather_attr.date, "%Y-%m-%d").day
            max_temperature_month = DateTimeUtil.month_name(
                date_string=weather_attr.date,
                date_format="%Y-%m-%d",
                short_name=False)
            print(
                f"{msg}: {weather_attr.value}{unit} on {max_temperature_month} {max_temperature_day}"
            )

    @classmethod
    def update_yearly_stats(cls, date, actual, current, relate=operator.lt):
        if helper.is_valid_int(current):
            if ((actual.value is None) or relate(actual.value, int(current))):
                actual.value = int(current)
                actual.date = date

    def calculate_year_stats(self):
        path = self.path_builder(with_month=False)
        month_files_list = FileUtil.file_names_list(path)

        if not month_files_list:
            return

        try:
            max_temperature = Stat(None, None)
            min_temperature = Stat(None, None)
            max_humidity = Stat(None, None)

            for file_path in month_files_list:
                with open(file_path, 'r') as file:
                    # Skip empty line, if on start of file
                    FileUtil.skip_blank_line(file)

                    reader = csv.DictReader(file, delimiter=',')
                    for row in reader:
                        date = self.read_date(row)
                        current_max_temperature = row[
                            WEATHER_FILE_HEADERS['MaxTemperatureC']]
                        current_min_temperature = row[
                            WEATHER_FILE_HEADERS['MinTemperatureC']]
                        current_max_humidity = row[
                            WEATHER_FILE_HEADERS['MaxHumidity']]

                        self.update_yearly_stats(date, max_temperature,
                                                 current_max_temperature)
                        self.update_yearly_stats(date, min_temperature,
                                                 current_min_temperature,
                                                 operator.gt)
                        self.update_yearly_stats(date, max_humidity,
                                                 current_max_humidity)

            self.print_year_stats(max_temperature, "Highest", "C")
            self.print_year_stats(min_temperature, "Lowest", "C")
            self.print_year_stats(max_humidity, "Humid", "%")

        except ValueError as exp:
            self.print_error(exp, path)
        except IOError as exp:
            self.print_error(exp, path)
            sys.exit()
