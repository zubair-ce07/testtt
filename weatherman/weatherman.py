import calendar
import csv

from termcolor import colored

from day_weather import DayWeather


class WeatherReport:
    weather_files = []

    def __init__(self, file_names):
        self.weather_files = file_names

    def __read_month_weather(self, month_weather_file):
        month_weather = []

        file_name = month_weather_file.split('/')[1]
        if file_name not in self.weather_files:
            return

        with open(month_weather_file) as csv_weather_file:
            raw_month_weather = csv.DictReader(csv_weather_file)
            for day_weather in raw_month_weather:
                month_weather.append(day_weather)
        return month_weather

    def print_annual_report(self, annual_weather):
        report_pattern = '{}: {}{} on {} {}'

        max_temp_day = annual_weather['max_temperature']
        min_temp_day = annual_weather['min_temperature']
        max_humidity_day = annual_weather['max_humidity']

        max_temp = max_temp_day.max_temperature
        min_temp = min_temp_day.min_temperature
        max_humidity = max_humidity_day.max_humidity

        max_temp_month = calendar.month_name[max_temp_day.get_month_number()]
        min_temp_month = calendar.month_name[min_temp_day.get_month_number()]
        max_humidity_month = calendar.month_name[max_humidity_day.get_month_number()]

        max_temp_day_num = max_temp_day.get_day_number()
        min_temp_day_num = min_temp_day.get_day_number()
        max_humid_day_num = max_humidity_day.get_day_number()

        print(report_pattern.format('Highest', max_temp, 'C', max_temp_month, max_temp_day_num))

        print(report_pattern.format('Lowest', min_temp, 'C', min_temp_month, min_temp_day_num))

        print(report_pattern.format('Humidity', max_humidity, '%', max_humidity_month, max_humid_day_num))

    def __print_average_month_weather(self, average_month_weather):
        report_pattern = '{}: {}{}'

        average_mean_humidity = average_month_weather['average_mean_humidity']
        average_max_temperature = average_month_weather['average_max_temperature']
        average_min_temperature = average_month_weather['average_min_temperature']

        print(report_pattern.format('Average Mean Humidity', average_mean_humidity, '%'))
        print(report_pattern.format('Highest Average', average_max_temperature, 'C'))
        print(report_pattern.format('Lowest Average', average_min_temperature, 'C'))

    def print_daily_weather_bonus(self, year_and_month, files_path):
        month_weather_details = self.get_month_weather_details(year_and_month, files_path)
        if not month_weather_details:
            print('Given month is not in the files')
            return

        year, month_name, month_weather = month_weather_details
        print(month_name + ' ' + year)

        for i in range(len(month_weather)):
            max_temp = month_weather[i].max_temperature
            min_temp = month_weather[i].min_temperature

            red_plus = colored('+' * max_temp, 'red')
            blue_plus = colored('+' * min_temp, 'blue')

            report_pattern = '{} {}{} {}C - {}C'
            print(report_pattern.format(i + 1, red_plus, blue_plus, max_temp, min_temp))

    def print_daily_weather(self, year_and_month, files_path):
        month_weather_details = self.get_month_weather_details(year_and_month, files_path)
        if not month_weather_details:
            print('Given month is not in the files')
            return

        year, month_name, month_weather = month_weather_details
        print(month_name + ' ' + year)

        for i in range(len(month_weather)):
            max_temp = month_weather[i].max_temperature
            min_temp = month_weather[i].min_temperature

            red_plus = colored('+' * max_temp, 'red')
            blue_plus = colored('+' * min_temp, 'blue')

            report_pattern = '{} {} {}C\n{} {} {}C'
            print(report_pattern.format(i + 1, red_plus, max_temp, i + 1, blue_plus, min_temp))

    def __compute_average_weather(self, month_weather):
        max_temperature_sum = sum(day_weather.max_temperature for day_weather in month_weather)
        min_temperature_sum = sum(day_weather.min_temperature for day_weather in month_weather)
        mean_humidity_sum = sum(day_weather.mean_humidity for day_weather in month_weather)

        total_days = len(month_weather)

        average_max_temperature = max_temperature_sum // total_days
        average_min_temperature = min_temperature_sum // total_days
        average_mean_humidity = mean_humidity_sum // total_days

        average_weather = dict()
        average_weather['average_max_temperature'] = average_max_temperature
        average_weather['average_min_temperature'] = average_min_temperature
        average_weather['average_mean_humidity'] = average_mean_humidity

        return average_weather

    def validate_month_day(self, day_weather):
        if day_weather['Max TemperatureC'] and day_weather['Min TemperatureC'] \
                and day_weather[' Mean Humidity']:
            return True

    def validate_year_day(self, day_weather):
        if day_weather['Max TemperatureC'] and day_weather['Min TemperatureC'] \
                and day_weather['Max Humidity']:
            return True

    def get_month_weather_details(self, year_and_month, files_path):
        month_weather = []
        year = year_and_month.split('/')[0]
        month = year_and_month.split('/')[1].replace('0', '')
        month_name = calendar.month_name[int(month)][: 3]

        complete_file_path = '{}/Murree_weather_{}_{}.txt'.format(files_path, year, month_name)

        raw_month_weather = self.__read_month_weather(complete_file_path)
        if not raw_month_weather:
            return

        for day_weather in raw_month_weather:
            if self.validate_month_day(day_weather):
                month_weather.append(DayWeather(day_weather))

        month_name = calendar.month_name[int(month)]
        return year, month_name, month_weather

    def get_annual_weather_insights(self, year, files_path):
        year_weather = []
        required_file_names = [weather_file for weather_file in self.weather_files if year in weather_file]

        for file_name in required_file_names:
            month_weather = self.__read_month_weather(files_path + '/' + file_name)
            for day_weather in month_weather:
                if self.validate_year_day(day_weather):
                    year_weather.append(DayWeather(day_weather))

        if not year_weather:
            return

        highest_temperature_day = max(year_weather, key=lambda day_weather_: day_weather_.max_temperature)
        lowest_temperature_day = min(year_weather, key=lambda day_weather_: day_weather_.min_temperature)
        highest_humidity_day = max(year_weather, key=lambda day_weather_: day_weather_.max_humidity)

        annual_weather = dict()
        annual_weather['max_temperature'] = highest_temperature_day
        annual_weather['min_temperature'] = lowest_temperature_day
        annual_weather['max_humidity'] = highest_humidity_day

        return annual_weather

    def get_average_month_weather(self, year_and_month, files_path):
        weather_details = self.get_month_weather_details(year_and_month, files_path)
        if not weather_details:
            return

        year, month_name, month_weather = weather_details
        average_month_weather = self.__compute_average_weather(month_weather)
        return average_month_weather

    def execute_first_task(self, year, files_path):
        annual_weather = self.get_annual_weather_insights(year, files_path)

        if annual_weather:
            self.print_annual_report(annual_weather)
        else:
            print('Given year is not in record files')

    def execute_second_task(self, year_and_month, files_path):
        average_month_weather = self.get_average_month_weather(year_and_month, files_path)

        if average_month_weather:
            self.__print_average_month_weather(average_month_weather)
        else:
            print('Given month is not in the files')

    def execute_third_task(self, year_and_month, files_path):
        self.print_daily_weather(year_and_month, files_path)

    def execute_bonus_task(self, year_and_month, files_path):
        self.print_daily_weather_bonus(year_and_month, files_path)
