import glob
import sys
import csv
from dataclasses import dataclass

from constants import WEATHER_FILE_HEADERS
from constants import MONTHS
from constants import COLORS
from constants import TEMPERATURE_SYMBOL

from helper import calculate_avg
from helper import file_handle
from helper import colored_string

@dataclass
class Stat:
    value: int
    date: str

class WeatherReport:
    def __init__(self,  _date, _files_path):
        self.files_path = _files_path
        self.date = _date

    def print_bar_chart(self, day, max_temperature, min_temperature):
        def print_temperature(day, color, temp):
            if(temp):
                print(f"{day.zfill(2)} {colored_string(TEMPERATURE_SYMBOL, color, temp)} {temp}C")

        def print_temperature_one_line(day, max_temperature_color, max_temperature, min_temperature_color, min_temperature):
            if(day and (max_temperature  or min_temperature)):
                bar = f"{day.zfill(2)} "
                if(max_temperature):
                    bar += f"{colored_string(TEMPERATURE_SYMBOL, max_temperature_color, max_temperature)}"
                if(min_temperature):
                    bar += f"{colored_string(TEMPERATURE_SYMBOL, min_temperature_color, min_temperature)}"
                if(max_temperature):
                    bar += f" {max_temperature}C"
                if(min_temperature):
                    if(max_temperature):
                        bar += ' - '
                    bar += f"{min_temperature}C"

                print(bar)

        print_temperature(day, COLORS['RED'], max_temperature)
        print_temperature(day, COLORS['BLUE'], min_temperature)
        print_temperature_one_line(day, COLORS['RED'], max_temperature, COLORS['BLUE'], min_temperature)

    def calc_month_min_max_stats(self):
        year, month = self.date.split('/')

        try:
            if(int(month) > 12 or int(month) < 1):
                print("Invalid month", int(month))
                return
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return

        short_month = MONTHS[int(month)][1]
        full_month =  MONTHS[int(month)][0]
        file_name = f"{self.files_path}/lahore_weather_{year}_{short_month}.txt"
        file_path = glob.glob(file_name)

        if not file_path:
            print("File not found", file_name)
            return
        else:
            file_path = file_path[0]

        f = file_handle(file_path)
        with f:
            try:
                f.readline() # Skip empty line on start
                reader = csv.DictReader(f, delimiter=',')
                print(f"{full_month} {year}")
                for row in reader:
                    date = row[WEATHER_FILE_HEADERS['Date']].split('-')[-1]
                    max_temperature = row[WEATHER_FILE_HEADERS['MaxTemperatureC']]
                    min_temperature = row[WEATHER_FILE_HEADERS['MinTemperatureC']]

                    if(date):
                        self.print_bar_chart(date, max_temperature, min_temperature)
            except Exception as exp:
                print("Unexpected error while parsing file:", str(exp), "file: ", file_path)

    def calc_month_avg_stats(self):
        year, month = self.date.split('/')

        try:
            if(int(month) > 12 or int(month) < 1):
                print("Invalid month", int(month))
                return
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return

        short_month = MONTHS[int(month)][1]
        file_name = f"{self.files_path}/lahore_weather_{year}_{short_month}.txt"
        file_path = glob.glob(file_name)

        if not file_path:
            print("File not found", file_name)
            return
        else:
            file_path = file_path[0]

        total_highest_temp = 0
        highest_temperature_count = 0

        total_lowest_temp = 0
        lowest_temperature_count = 0

        total_humidity = 0
        humidity_count = 0

        f = file_handle(file_path)
        with f:
            try:
                f.readline() # Skip empty line on start
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    max_temperature = row[WEATHER_FILE_HEADERS['MaxTemperatureC']]
                    min_temperature = row[WEATHER_FILE_HEADERS['MinTemperatureC']]
                    humidity = row[WEATHER_FILE_HEADERS['MeanHumidity']]

                    if max_temperature:
                        total_highest_temp += int(max_temperature)
                        highest_temperature_count += 1

                    if min_temperature:
                        total_lowest_temp += int(min_temperature)
                        lowest_temperature_count += 1

                    if humidity:
                        total_humidity += int(humidity)
                        humidity_count += 1
            except Exception as exp:
                print("Unexpected error while parsing file:", str(exp), "file: ", file_path)

        avg_highest_temp = calculate_avg(total_highest_temp, highest_temperature_count)
        avg_lowest_temp = calculate_avg(total_lowest_temp, lowest_temperature_count)
        avg_humidity = calculate_avg(total_humidity, humidity_count)

        print(f"Highest Average: {avg_highest_temp}C")
        print(f"Lowest Average: {avg_lowest_temp}C")
        print(f"Average Humidity: {avg_humidity}%")

    def calculate_year_stats(self):
        year = self.date.split('/')[0]
        file_names = f"{self.files_path}/lahore_weather_{year}_*.txt"
        month_files_list = glob.glob(file_names)

        if(not(month_files_list)):
            print(f"No data found for: {year}")
            return

        max_temperature = Stat(None, None)
        min_temperature = Stat(None, None)
        max_humidity = Stat(None, None)


        for month_file in month_files_list:
            f = file_handle(month_file)
            with f:
                try:
                    f.readline() # Skip empty line on start
                    reader = csv.DictReader(f, delimiter=',')
                    for row in reader:
                        date = row[WEATHER_FILE_HEADERS['Date']]
                        current_max_temperature = row[WEATHER_FILE_HEADERS['MaxTemperatureC']]
                        current_min_temperature = row[WEATHER_FILE_HEADERS['MinTemperatureC']]
                        current_max_humidity = row[WEATHER_FILE_HEADERS['MaxHumidity']]

                        if (current_max_temperature):
                            if((max_temperature.value is None) or (max_temperature.value  < int(current_max_temperature))):
                                max_temperature.value  = int(current_max_temperature)
                                max_temperature.date = date

                        if (current_min_temperature):
                            if((min_temperature.value is None) or (min_temperature.value  < int(current_min_temperature))):
                                min_temperature.value  = int(current_min_temperature)
                                min_temperature.date = date

                        if (current_max_humidity):
                            if((max_humidity.value is None) or max_humidity.value  < int(current_max_humidity)):
                                max_humidity.value  = int(current_max_humidity)
                                max_humidity.date = date
                except Exception as exp:
                    print("Unexpected error while parsing file:", str(exp), "file: ", month_file)

        if(max_temperature.value and max_temperature.date):
            max_temperature_month, max_temperature_day = max_temperature.date.split('-')[-2:]
            max_temperature_month = MONTHS[int(max_temperature_month)][0]
            print(f"Highest: {max_temperature.value}C on {max_temperature_month} {max_temperature_day}")

        if(min_temperature.value and min_temperature.date):
            min_temperature_month, min_temperature_day = min_temperature.date.split('-')[-2:]
            min_temperature_month = MONTHS[int(min_temperature_month)][0]
            print(f"Lowest: {min_temperature.value}C on {min_temperature_month} {min_temperature_day}")

        if(max_humidity.value and max_humidity.date):
            max_humidity_month, max_humid_day = max_humidity.date.split('-')[-2:]
            max_humidity_month = MONTHS[int(max_humidity_month)][0]
            print(f"Humid: {max_humidity.value}% on {max_humidity_month} {max_humid_day}")
