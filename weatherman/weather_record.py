import os
from termcolor import colored
from weather import Weather


class WeatherRecord:

    def __init__(self, path_to_files):
        self.past_weather_data = []
        self.file_names = {}
        self.MONTH_NAMES_MAP = {
                            'Jan': 1, 'Feb': 2, 'Mar': 3,
                            'Apr': 4, 'May': 5, 'Jun': 6,
                            'Jul': 7, 'Aug': 8, 'Sep': 9,
                            'Oct': 10, 'Nov': 11, 'Dec': 12
                            }
        self.create_file_map(path_to_files)

    def create_file_map(self, path_to_files):
        # keeps track of weather files
        for root, dirs, files in os.walk(path_to_files):
            for file_name in files:
                weather_file_name = path_to_files + file_name

                split_file_name = weather_file_name.split('_')
                year = split_file_name[-2]
                month = split_file_name[-1].split('.')[0]

                month = self.MONTH_NAMES_MAP[month]

                if year not in self.file_names:
                    self.file_names[year] = {}

                self.file_names[year][month] = weather_file_name

    def retrieve_weather_data_from_file(self, weather_curr_day, year):
        # Simply extracting weather_record
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

    def get_year(self, date):
        year = date.split('/')[0]

        if year not in self.file_names:
            print "-------------No Relevant Data Found--------------"
            print "Check if you're giving correct year and data path"
            exit(2)

        return year

    def get_month(self, date, year):
        split_date = date.split('/')
        if len(split_date) > 1:
            month = int(split_date[1])

            if month not in self.file_names[year]:
                print "-------No Relevant Data Found-------"
                print "Check if you're giving correct month"
                exit(2)

            return month
        else:
            print "-----No Relevant Data Found-----"
            print "Month not specified in the input"
            exit(2)

    def print_monthly_report(self, date):
        year = self.get_year(date)
        month = self.get_month(date, year)

        file_name = self.file_names[year][month]

        with open(file_name) as weather_file_data:
            for weather_curr_day in weather_file_data:
                weather = self.retrieve_weather_data_from_file(weather_curr_day, year)
                if weather:
                    self.past_weather_data.append(weather)

        print date
        for weather in self.past_weather_data:
            if weather.year + "/" + weather.month == date:
                print(weather.day + " " +
                      colored('+' * int(weather.min_temp), 'blue') +
                      colored('+' * int(weather.max_temp), 'red') +
                      str(weather.min_temp) + "C - " +
                      str(weather.max_temp) + "C")

    def print_extreme_weather_report(self, date):
        year = self.get_year(date)

        for month in self.file_names[year]:
            file_name = self.file_names[year][month]
            with open(file_name) as weather_file_data:
                for weather_curr_day in weather_file_data:
                    weather = self.retrieve_weather_data_from_file(weather_curr_day, year)
                    if weather:
                        self.past_weather_data.append(weather)

        (max_temp, min_temp,
         max_humidity, max_temp_day,
         min_temp_day, max_humid_day) = self.get_extreme_weather()

        print "Highest : " + str(max_temp) + "C on " + max_temp_day
        print "Lowest : " + str(min_temp) + "C on " + min_temp_day
        print "Humid : " + str(max_humidity) + "% on " + max_humid_day

    def print_average_weather_report(self, date):
        year = self.get_year(date)
        month = self.get_month(date, year)

        file_name = self.file_names[year][month]

        with open(file_name) as weather_file_data:
            for weather_curr_day in weather_file_data:
                weather = self.retrieve_weather_data_from_file(weather_curr_day, year)
                if weather:
                    self.past_weather_data.append(weather)

        (max_mean_temp,
         min_mean_temp,
         mean_humidity) = self.get_average_weather()

        print "Highest Average : " + str(max_mean_temp)
        print "Lowest Average : " + str(min_mean_temp)
        print "Average Humidity : " + str(mean_humidity)

    def get_average_weather(self):
        max_mean_temp, min_mean_temp, mean_humidity = -273, 50, 0

        weather = max(self.past_weather_data, key=lambda x: int(x.mean_temp))
        max_mean_temp = weather.max_temp

        weather = min(self.past_weather_data, key=lambda x: int(x.mean_temp))
        min_mean_temp = weather.min_temp

        mean_humidity = sum(int(x.mean_humidity)
                            for x in self.past_weather_data)
        mean_humidity /= len(self.past_weather_data)

        return max_mean_temp, min_mean_temp, mean_humidity

    def get_extreme_weather(self):
        max_temp, min_temp, max_humidity = -273, 50, 0
        max_temp_day, min_temp_day, max_humid_day = None, None, None

        weather = max(self.past_weather_data, key=lambda x: int(x.max_temp))
        max_temp_day = weather.MONTH_NAMES_MAP[weather.month] + " " + weather.day
        max_temp = weather.max_temp

        weather = min(self.past_weather_data, key=lambda x: int(x.min_temp))
        min_temp_day = weather.MONTH_NAMES_MAP[weather.month] + " " + weather.day
        min_temp = weather.min_temp

        weather = max(self.past_weather_data,
                      key=lambda x: int(x.max_humidity))
        max_humid_day = weather.MONTH_NAMES_MAP[weather.month] + " " + weather.day
        max_humidity = weather.max_humidity

        return (max_temp, min_temp,
                max_humidity, max_temp_day,
                min_temp_day, max_humid_day)
