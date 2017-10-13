import calendar
import csv
import re

from termcolor import colored

from day_weather import DayWeather


class WeatherReport:
    weather_files = []

    def __init__(self, file_names):
        self.weather_files = file_names

    def __read_month_weather(self, month_weather_file):
        month_weather = []
        try:
            with open(month_weather_file) as csv_weather_file:
                raw_month_weather = csv.DictReader(csv_weather_file)
                for day_weather in raw_month_weather:
                    month_weather.append(day_weather)
        except:
            print('Given file not Found')
        return month_weather

    def __compute_average_weather(self, month_weather):
        max_temperature_sum = sum(day_weather.max_temperature for day_weather in month_weather)
        min_temperature_sum = sum(day_weather.min_temperature for day_weather in month_weather)
        mean_humidity_sum = sum(day_weather.mean_humidity for day_weather in month_weather)

        total_days = len(month_weather)

        average_max_temperature = max_temperature_sum // total_days
        average_min_temperature = min_temperature_sum // total_days
        average_mean_humidity = mean_humidity_sum // total_days

        report_pattern = '{}: {}{}'

        print(report_pattern.format('Average Mean Humidity', average_mean_humidity, '%'))
        print(report_pattern.format('Highest Average', average_max_temperature, 'C'))
        print(report_pattern.format('Lowest Average', average_min_temperature, 'C'))

    def print_annual_report(self, highest_temp_day, lowest_temp_day, highest_humidity_day):
        report_pattern = '{}: {}{} on {} {}'

        print(report_pattern.format('Highest', highest_temp_day.max_temperature, 'C',
                                    calendar.month_name[highest_temp_day.get_month_number()],
                                    highest_temp_day.get_day_number()))

        print(report_pattern.format('Lowest', lowest_temp_day.min_temperature, 'C',
                                    calendar.month_name[lowest_temp_day.get_month_number()],
                                    lowest_temp_day.get_day_number()))

        print(report_pattern.format('Humidity', highest_humidity_day.max_humidity, '%',
                                    calendar.month_name[highest_humidity_day.get_month_number()],
                                    highest_humidity_day.get_day_number()))

    def get_month_weather_details(self, year_and_month, files_path):
        month_weather = []
        year = year_and_month.split('/')[0]
        month = year_and_month.split('/')[1].replace('0', '')
        try:
            month_name = calendar.month_name[int(month)][: 3]
        except:
            print('Given month is incorrect')
            return None

        complete_file_path = '{}/Murree_weather_{}_{}.txt'.format(files_path, year, month_name)

        raw_month_weather = self.__read_month_weather(complete_file_path)
        for day_weather in raw_month_weather:
            if day_weather['Max TemperatureC'] and day_weather['Min TemperatureC'] \
                    and day_weather[' Mean Humidity']:
                month_weather.append(DayWeather(day_weather))

        month_name = calendar.month_name[int(month)]

        return year, month_name, month_weather

    def print_daily_weather_bonus(self, year, month_name, month_weather):
        print(month_name + ' ' + year)
        for i in range(len(month_weather)):
            max_temp = month_weather[i].max_temperature
            min_temp = month_weather[i].min_temperature
            if max_temp and min_temp:
                report_pattern = '{} {} {}C - {}C'
                print(report_pattern.format(i + 1, colored('+' * int(max_temp), 'red') +
                                            colored('+' * int(min_temp), 'blue'), max_temp,
                                            min_temp))

    def print_daily_weather(self, year, month_name, month_weather):
        print(month_name + ' ' + year)
        for i in range(len(month_weather)):
            max_temp = month_weather[i].max_temperature
            min_temp = month_weather[i].min_temperature
            if max_temp and min_temp:
                report_pattern = '{} {} {}C\n{} {} {}C'
                print(report_pattern.format(i + 1, colored('+' * int(max_temp), 'red'), max_temp,
                                            i + 1, colored('+' * int(min_temp), 'blue'), min_temp))

    def get_annual_weather_insights(self, year, files_path):
        year_weather = []

        for file_name in self.weather_files:
            if year == file_name.split('_')[2]:
                month_weather = self.__read_month_weather(files_path + '/' + file_name)
                for day_weather in month_weather:
                    if day_weather['Max TemperatureC'] and day_weather['Min TemperatureC'] \
                            and day_weather['Max Humidity']:
                        year_weather.append(DayWeather(day_weather))

        if year_weather:
            highest_temperature_day = max(year_weather, key=lambda day_weather_: day_weather_.max_temperature)
            lowest_temperature_day = min(year_weather, key=lambda day_weather_: day_weather_.min_temperature)
            highest_humidity_day = max(year_weather, key=lambda day_weather_: day_weather_.max_humidity)

            self.print_annual_report(highest_temperature_day, lowest_temperature_day, highest_humidity_day)
        else:
            print('Given year is not in record files')

    def get_monthly_weather_insights(self, year_and_month, files_path):
        weather_details = self.get_month_weather_details(year_and_month, files_path)

        if weather_details:
            year, month_name, month_weather = weather_details
            self.__compute_average_weather(month_weather)
        else:
            print('Given month is not in the files')

    def days_insights_single_line_chart(self, year_and_month, files_path):
        weather_details = self.get_month_weather_details(year_and_month, files_path)
        if weather_details:
            year, month_name, month_weather = weather_details
            self.print_daily_weather_bonus(year, month_name, month_weather)

    def days_insights_double_line_chart(self, year_and_month, files_path):
        weather_details = self.get_month_weather_details(year_and_month, files_path)
        if weather_details:
            year, month_name, month_weather = weather_details
            self.print_daily_weather(year, month_name, month_weather)

    def execute_first_task(self, year, files_path):
        pattern = re.compile('\d{4}$')
        if pattern.match(year):
            self.get_annual_weather_insights(year, files_path)
        else:
            print('Error >> usage: -e year')

    def validate_year_and_month(self, year_and_month):
        pattern = re.compile('\d{4}/\d{1,2}$')
        if pattern.match(year_and_month):
            return True
        else:
            print('Error >> usage: [-option] year/month')
            return False

    def execute_second_task(self, year_and_month, files_path):
        if self.validate_year_and_month(year_and_month):
            self.get_monthly_weather_insights(year_and_month, files_path)

    def execute_third_task(self, year_and_month, files_path):
        if self.validate_year_and_month(year_and_month):
            self.days_insights_double_line_chart(year_and_month, files_path)

    def execute_bonus_task(self, year_and_month, files_path):
        if self.validate_year_and_month(year_and_month):
            self.days_insights_single_line_chart(year_and_month, files_path)
