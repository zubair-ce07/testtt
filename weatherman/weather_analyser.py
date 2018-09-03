import os
import glob
import csv
import calendar
from datetime import datetime
from weather_data import WeatherData


class WeatherAnalyser:

    def get_weather_date(self, date_string):
        date = datetime.strptime(date_string, '%Y-%m-%d')
        return date.year, date.month, date.day

    def get_files_for_yearly_weather(self, year, weather_files_path):
        weather_files = []
        try:
            os.chdir(weather_files_path)
            files_pattern = 'Murree_weather_'+year+'_*.txt'
            file_names = glob.glob(files_pattern)

        except FileNotFoundError:
            print('Files path is incorrect')
        for weather_file in file_names:
            with open((weather_files_path + weather_file)) as csv_file:
                month_weather = list(csv.reader(csv_file, delimiter=','))
                weather_year, _, _ = self.get_weather_date(month_weather[1][0])
                if int(year) == weather_year:
                    weather_files.append(weather_file)
        return weather_files

    def calculate_weather_data_for_year_(self, year, weather_files_path):
        weather_files = self.get_files_for_yearly_weather(year, weather_files_path)
        yearly_weather_data = []
        for weather_file in weather_files:
            yearly_weather_data.extend(
                self.calculate_month_weather_data(weather_files_path, weather_file)
            )
        max_temperature_data = [
            day_weather for day_weather in yearly_weather_data if
            day_weather.get_max_temperature()
        ]
        highest = max(
            max_temperature_data,
            key=lambda day_weather: int(day_weather.get_max_temperature())
        )
        min_temperature_data = [
            day_weather for day_weather in yearly_weather_data if
            day_weather.get_min_temperature()
        ]
        lowest = min(
            min_temperature_data,
            key=lambda day_weather: int(day_weather.get_min_temperature())
        )
        most_humidity_data = [
            day_weather for day_weather in yearly_weather_data if
            day_weather.get_humidity()
        ]
        humid = max(
            most_humidity_data,
            key=lambda day_weather: int(day_weather.get_humidity())
        )
        return (highest, lowest, humid)

    def get_file_for_monthly_data(self, year, month, weather_files_path):

        try:
            os.chdir(weather_files_path)
            files_pattern = 'Murree_weather_' + year + '_' + calendar.month_abbr[int(month)] + '.txt'
            file_names = glob.glob(files_pattern)

        except FileNotFoundError:
            print('Files path or year/month is incorrect')
        for weather_file in file_names:
            with open(weather_files_path + weather_file) as csv_file:
                month_weather = list(csv.reader(csv_file, delimiter=','))
                weather_year, weather_month, _ = self.get_weather_date(month_weather[1][0])
                if int(year) == weather_year and int(month) == weather_month:
                    return weather_file

    def calculate_month_weather_data(self, weather_files_path, weather_file):
        month_weather_data = []
        with open(weather_files_path + weather_file) as csv_file:
            month_weather = csv.reader(csv_file, delimiter=',')
            month_weather = list(month_weather)
            for day_weather in month_weather[1:]:
                month_weather_data.append(
                    WeatherData(
                        day_weather[0], day_weather[1],
                        day_weather[3], day_weather[7]
                    )
                )
        return month_weather_data

    def calculate_weather_data_averages(self, year, month, weather_files_path):
        weather_file = self.get_file_for_monthly_data(year, month, weather_files_path)
        month_weather_data = self.calculate_month_weather_data(weather_files_path, weather_file)
        month_high_temperature_data = [
            int(day_weather.get_max_temperature()) for day_weather in
            month_weather_data if day_weather.get_max_temperature()
        ]
        month_low_temperature_data = [
            int(day_weather.get_min_temperature()) for day_weather in
            month_weather_data if day_weather.get_min_temperature()
        ]
        month_humidity_data_data = [
            int(day_weather.get_humidity()) for day_weather in
            month_weather_data if day_weather.get_humidity()
        ]
        highest_average = int(sum(month_high_temperature_data) / len(month_high_temperature_data))
        lowest_average = int(sum(month_low_temperature_data) / len(month_low_temperature_data))
        humidity_average = int(sum(month_humidity_data_data) / len(month_humidity_data_data))
        weather_averages = {
            "Highest Average" : highest_average,
            "Lowest Average" : lowest_average,
            "Average Humidity": humidity_average
        }
        return weather_averages

    def calculate_weather_data_for_bars(self, year, month, weather_files_path):
        weather_file = self.get_file_for_monthly_data(year, month, weather_files_path)
        month_weather_data = self.calculate_month_weather_data(weather_files_path, weather_file)
        return month_weather_data

    def generate_daily_report_bar(self,date, colour, temperature):
        GRAY = " \033[00m"
        bar = int(temperature) * "+" if temperature else temperature
        return "{} {}{}{}{}C".format(date, colour, bar, GRAY, temperature)

    def generate_daily_report_bounas_bar(self,date, max_temperature, min_temperature):
        BLUE = "\033[96m"
        GRAY = " \033[00m"
        RED = "\033[91m"
        min_bar = int(min_temperature) * "+" if min_temperature else min_temperature
        max_bar = int(max_temperature) * "+" if max_temperature else max_temperature
        min_temperature = min_temperature + "-" if min_temperature else ""
        return "{} {}{}{}{}{}{}{}C".format(date, BLUE, min_bar, RED,max_bar,GRAY, min_temperature, max_temperature)

