import os
from termcolor import colored
from weather import Weather, MONTH_NAMES_MAP as number_to_name_map

MONTH_NAMES_MAP = {
                   'Jan': 1, 'Feb': 2, 'Mar': 3,
                   'Apr': 4, 'May': 5, 'Jun': 6,
                   'Jul': 7, 'Aug': 8, 'Sep': 9,
                   'Oct': 10, 'Nov': 11, 'Dec': 12
                  }


class WeatherRecord:

    def __init__(self, path_to_files):
        self.file_names = {}
        self.create_file_map(path_to_files)

    def create_file_map(self, path_to_files):
        # keeps track of weather files
        for root, dirs, files in os.walk(path_to_files):
            for file_name in files:
                weather_file_name = path_to_files + file_name

                split_file_name = weather_file_name.split('_')
                year = split_file_name[-2]
                month = split_file_name[-1].split('.')[0]

                month = MONTH_NAMES_MAP[month]

                if year not in self.file_names:
                    self.file_names[year] = {}

                self.file_names[year][month] = weather_file_name

    def verify_year(self, year):
        if year not in self.file_names:
            print "-------------No Relevant Data Found--------------"
            print "Check if you're giving correct year and data path"
            exit(2)

        return True

    def verify_month(self, month, year):
        if month not in self.file_names[year]:
                print "-------No Relevant Data Found-------"
                print "Check if you're giving correct month"
                exit(2)
        return True

    def parse_weather_record_line(self, weather_curr_day, year):
        """Simply extracting weather_record"""
        weather_curr_day = weather_curr_day.split(',')

        if len(weather_curr_day) > 1:
            date = weather_curr_day[0].split('-')

            if len(date) > 1:
                day = date[-1]
                month = date[-2]

                max_temp = weather_curr_day[1]
                mean_temp = weather_curr_day[2]
                min_temp = weather_curr_day[3]

                max_humidity = weather_curr_day[7]
                mean_humidity = weather_curr_day[8]
                min_humidity = weather_curr_day[9]

                if (min_temp and max_temp and
                   min_humidity and max_humidity):
                    weather = Weather(day, month, year, max_temp,
                                      min_temp, mean_temp,
                                      max_humidity, min_humidity,
                                      mean_humidity)
                    return weather

    def parse_weather_record_file(self, file_name, year):

        with open(file_name) as weather_file_data:
            for weather_curr_day in weather_file_data:
                weather = self.parse_weather_record_line(weather_curr_day,
                                                         year)
                yield weather

    def print_monthly_report(self, year, month):

        if self.verify_year(year) and self.verify_month(month, year):
            file_name = self.file_names[year][month]
            weather_record_gen = self.parse_weather_record_file(file_name,
                                                                year)
            weather_data = []
            try:
                while True:
                    weather = next(weather_record_gen)
                    if weather:
                        weather_data.append(weather)
            except StopIteration:
                print str(year) + "/" + str(month)
                for weather in weather_data:
                    print(weather.day + " " +
                          colored('+' * int(weather.min_temp), 'blue') +
                          colored('+' * int(weather.max_temp), 'red') +
                          str(weather.min_temp) + "C - " +
                          str(weather.max_temp) + "C")

    def print_extreme_weather_report(self, year):
        weather_data = []

        for month in self.file_names[year]:
            file_name = self.file_names[year][month]
            weather_record_gen = self.parse_weather_record_file(file_name,
                                                                year)
            try:
                while True:
                    weather = next(weather_record_gen)
                    if weather:
                        weather_data.append(weather)
            except StopIteration:
                pass

        (max_temp, min_temp,
         max_humidity,
         max_temp_day,
         min_temp_day,
         max_humid_day) = self._get_extreme_weather(weather_data)

        print "Highest : " + str(max_temp) + "C on " + max_temp_day
        print "Lowest : " + str(min_temp) + "C on " + min_temp_day
        print "Humid : " + str(max_humidity) + "% on " + max_humid_day

    def print_average_weather_report(self, year, month):
        file_name = self.file_names[year][month]

        weather_record_gen = self.parse_weather_record_file(file_name,
                                                            year)
        weather_data = []
        try:
            while True:
                weather = next(weather_record_gen)
                if weather:
                    weather_data.append(weather)

        except StopIteration:
            (max_mean_temp,
             min_mean_temp,
             mean_humidity) = self._get_average_weather(weather_data)

            print "Highest Average : " + str(max_mean_temp)
            print "Lowest Average : " + str(min_mean_temp)
            print "Average Humidity : " + str(mean_humidity)

    def _get_average_weather(self, weather_data):
        max_mean_temp, min_mean_temp, mean_humidity = -273, 50, 0

        weather = max(weather_data, key=lambda x: int(x.mean_temp))
        max_mean_temp = weather.max_temp

        weather = min(weather_data, key=lambda x: int(x.mean_temp))
        min_mean_temp = weather.min_temp

        mean_humidity = sum(int(x.mean_humidity)
                            for x in weather_data) / len(weather_data)

        return max_mean_temp, min_mean_temp, mean_humidity

    def _get_extreme_weather(self, weather_data):
        max_temp, min_temp, max_humidity = -273, 50, 0
        max_temp_day, min_temp_day, max_humid_day = None, None, None

        weather = max(weather_data, key=lambda x: int(x.max_temp))
        max_temp_day = number_to_name_map[weather.month] + " " + weather.day
        max_temp = weather.max_temp

        weather = min(weather_data, key=lambda x: int(x.min_temp))
        min_temp_day = number_to_name_map[weather.month] + " " + weather.day
        min_temp = weather.min_temp

        weather = max(weather_data, key=lambda x: int(x.max_humidity))
        max_humid_day = number_to_name_map[weather.month] + " " + weather.day
        max_humidity = weather.max_humidity

        return (max_temp, min_temp,
                max_humidity, max_temp_day,
                min_temp_day, max_humid_day)
