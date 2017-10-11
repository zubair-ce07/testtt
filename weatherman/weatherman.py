import calendar
import csv

from termcolor import colored

from day_weather import DayWeatherRecord


class WeatherReport:
    weather_record_file_names = []

    def __init__(self, file_names):
        self.weather_record_file_names = file_names

    def __read_month_weather(self, month_weather_record_file_path):
        month_weather_record = []

        with open(month_weather_record_file_path) as csv_weather_file:
            raw_weather_record = csv.DictReader(csv_weather_file)
            for day_weather_record in raw_weather_record:
                month_weather_record.append(day_weather_record)

        return month_weather_record

    def __get_filtered_day_weather(self, raw_day_weather):
        return DayWeatherRecord(raw_day_weather)

    def __compute_average_weather(self, month_weather_record):
        max_temperature_sum = sum(
            int(day_weather_record.max_temperature) for day_weather_record in month_weather_record)
        min_temperature_sum = sum(
            int(day_weather_record.min_temperature) for day_weather_record in month_weather_record)
        mean_humidity_sum = sum(
            int(day_weather_record.mean_humidity) for day_weather_record in month_weather_record)

        total_days = len(month_weather_record)

        average_max_temperature = max_temperature_sum // total_days
        average_min_temperature = min_temperature_sum // total_days
        average_mean_humidity = mean_humidity_sum // total_days

        monthly_average_record = '{}: {}{}'

        print(monthly_average_record.format('Highest Average',
                                            average_max_temperature,
                                            'C'))
        print(monthly_average_record.format('Lowest Average',
                                            average_min_temperature,
                                            'C'))
        print(monthly_average_record.format('Average Mean Humidity',
                                            average_mean_humidity,
                                            '%'))

    def get_required_day(self, month_weather_record, option):
        if option == 1:
            return max(month_weather_record, key=lambda day_weather_record: int(day_weather_record.max_temperature))

        if option == 2:
            return min(month_weather_record, key=lambda day_weather_record: int(day_weather_record.min_temperature))

        if option == 3:
            return max(month_weather_record, key=lambda day_weather_record: int(day_weather_record.max_humidity))
        return month_weather_record[0]

    def print_yearly_report(self, highest_temp_day, lowest_temp_day, highest_humidity_day):
        yearly_report = '{}: {}{} on {} {}'

        print(yearly_report.format('Highest',
                                   highest_temp_day.max_temperature,
                                   'C',
                                   calendar.month_name[highest_temp_day.get_month_number()],
                                   highest_temp_day.get_day_number()))

        print(yearly_report.format('Lowest',
                                   lowest_temp_day.min_temperature,
                                   'C',
                                   calendar.month_name[lowest_temp_day.get_month_number()],
                                   lowest_temp_day.get_day_number()))

        print(yearly_report.format('Humidity',
                                   highest_humidity_day.max_humidity,
                                   '%',
                                   calendar.month_name[highest_humidity_day.get_month_number()],
                                   highest_humidity_day.get_day_number()))

    def get_month_weather_record(self, year_and_month, files_path):
        month_weather_record = []
        year = year_and_month.split('/')[0]
        month = year_and_month.split('/')[1]

        complete_weather_file_path = '{}/Murree_weather_{}_{}.txt'.format(files_path,
                                                                          year,
                                                                  calendar.month_name[int(month)][:3])

        raw_month_weather_record = self.__read_month_weather(complete_weather_file_path)
        for raw_day_weather_record in raw_month_weather_record:
            if raw_day_weather_record['Max TemperatureC'] and \
                    raw_day_weather_record['Min TemperatureC'] and \
                    raw_day_weather_record[' Mean Humidity']:
                month_weather_record.append(self.__get_filtered_day_weather(raw_day_weather_record))

        month_name = calendar.month_name[int(month)]

        return year, month_name, month_weather_record

    def print_dayily_weather_record(self, year, month_name, month_weather_record):
        print(month_name + ' ' + year)
        for i in range(len(month_weather_record)):
            max_temp = month_weather_record[i].max_temperature
            min_temp = month_weather_record[i].min_temperature
            day_record = '{} {} {}C - {}C'
            print(day_record.format(i + 1,
                                    colored('+' * int(max_temp), 'red') + colored('+' * int(min_temp), 'blue'),
                                    max_temp,
                                    min_temp))

    def get_yearly_weather_insights(self, year, files_path):
        year_weather_record = []

        for file_name in self.weather_record_file_names:
            month_weather_record = self.__read_month_weather(files_path + '/' + file_name)
            if year == file_name.split('_')[2]:
                for raw_day_weather_record in month_weather_record:
                    if raw_day_weather_record['Max TemperatureC'] and \
                            raw_day_weather_record['Min TemperatureC'] and \
                            raw_day_weather_record['Max Humidity']:
                        year_weather_record.append(self.__get_filtered_day_weather(raw_day_weather_record))

        highest_temperature_day = self.get_required_day(year_weather_record, 1)
        lowest_temperature_day = self.get_required_day(year_weather_record, 2)
        highest_humidity_day = self.get_required_day(year_weather_record, 3)

        self.print_yearly_report(highest_temperature_day, lowest_temperature_day, highest_humidity_day)

    def get_monthly_weather_insights(self, year_and_month, files_path):
        year, month_name, month_weather_record = self.get_month_weather_record(year_and_month, files_path)
        self.__compute_average_weather(month_weather_record)

    def get_days_weather_insights(self, year_and_month, files_path):
        year, month_name, month_weather_record = self.get_month_weather_record(year_and_month, files_path)
        self.print_dayily_weather_record(year, month_name, month_weather_record)
