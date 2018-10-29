#!/usr/bin/python3.6
import calendar
import datetime

from csv_file_data_holder import CsvFileDataHolder
from constants import MONTHS_NAME


class WeatherDataAnalysis:

    def analyse(self, operation, weather_readings, date):
        if operation == 'e':
            return self.calculate_yearly_record(weather_readings, date.year)
        elif operation == 'a':
            return self.calculate_monthly_record(weather_readings, date)
        elif operation == 'c':
            return self.calculate_monthly_record_for_bar_charts(weather_readings, date)

    def yearly_highest_temp_struct(self, date_values, month_data, year_max_temp, highest_temp_struct):
        max_temp_list = month_data.get_int_converted_attribute_values(
            'Max TemperatureC')
        month_max_temp = max(list(filter(None.__ne__, max_temp_list)))
        if year_max_temp <= month_max_temp:
            date = max_temp_list.index(month_max_temp)
            date_value = datetime.datetime.strptime(
                date_values[date], '%Y-%m-%d')
            highest_temp_struct = [month_max_temp, date_value]
        return highest_temp_struct

    def yearly_lowest_temp_struct(self, date_values, month_data, year_min_temp, lowest_temp_struct):
        min_temp_list = month_data.get_int_converted_attribute_values(
            'Min TemperatureC')
        month_min_temp = min(list(filter(None.__ne__, min_temp_list)))
        if year_min_temp >= month_min_temp:
            date = min_temp_list.index(month_min_temp)
            date_value = datetime.datetime.strptime(
                date_values[date], '%Y-%m-%d')
            lowest_temp_struct = [month_min_temp, date_value]
        return lowest_temp_struct

    def yearly_most_humid_struct(self, date_values, month_data, year_highest_humidity, most_humid_struct):
        highest_humidity_list = month_data.get_int_converted_attribute_values(
            'Max Humidity')
        month_highest_humid_day = max(list(filter(None.__ne__,
                                                  highest_humidity_list)))
        if year_highest_humidity <= month_highest_humid_day:
            date = highest_humidity_list.index(month_highest_humid_day)
            date_value = datetime.datetime.strptime(
                date_values[date], '%Y-%m-%d')
            most_humid_struct = [month_highest_humid_day, date_value]
        return most_humid_struct

    def calculate_yearly_record(self, weather_readings, year):
        highest_temp_struct, lowest_temp_struct = [], []
        most_humid_struct, report = [], []
        year_max_temp, year_min_temp, year_highest_humidity = -273, 200, 0
        months_data = weather_readings.get_months_data_of_year(year)
        for month in months_data:
            month_data = months_data.get(month)
            if month_data is not None:
                key = [val for val in month_data.data.keys() if 'PK' in val]
                date_values = month_data.data.get(key[0])
                highest_temp_struct = self.yearly_highest_temp_struct(
                    date_values, month_data, year_max_temp, highest_temp_struct)
                year_max_temp = highest_temp_struct[0]
                lowest_temp_struct = self.yearly_lowest_temp_struct(
                    date_values, month_data, year_min_temp, lowest_temp_struct)
                year_min_temp = lowest_temp_struct[0]
                most_humid_struct = self.yearly_most_humid_struct(
                    date_values, month_data, year_highest_humidity, most_humid_struct)
                year_highest_humidity = most_humid_struct[0]
                report = [highest_temp_struct,
                          lowest_temp_struct,
                          most_humid_struct]
        return report

    def calculate_monthly_record(self, weather_readings, date):
        months = weather_readings.get_months_data_of_year(date.year)
        report = []
        month = months.get(calendar.month_name[date.month])
        if month is not None:
            max_temp_list = month.get_int_converted_attribute_values(
                'Max TemperatureC')
            min_temp_list = month.get_int_converted_attribute_values(
                'Min TemperatureC')
            mean_humidty_list = month.get_int_converted_attribute_values(
                'Mean Humidity')
            report.append(sum(list(filter(None.__ne__, max_temp_list)))
                          / len(list(filter(None.__ne__, max_temp_list))))
            report.append(sum(list(filter(None.__ne__, min_temp_list)))
                          / len(list(filter(None.__ne__, min_temp_list))))
            report.append(sum(list(filter(None.__ne__, mean_humidty_list)))
                          / len(list(filter(None.__ne__, mean_humidty_list))))
        return report

    def calculate_monthly_record_for_bar_charts(self, weather_readings, date):
        months = weather_readings.get_months_data_of_year(date.year)
        report = {}
        month = months.get(calendar.month_name[date.month])
        if month is not None:
            max_temp_list = month.get_int_converted_attribute_values(
                'Max TemperatureC')
            min_temp_list = month.get_int_converted_attribute_values(
                'Min TemperatureC')
            report['high_temprature'] = max_temp_list
            report['low_temprature'] = min_temp_list
        return report
