#!/usr/bin/python3.6
import calendar
import datetime

from csv_file_data_holder import CsvFileDataHolder


class WeatherDataAnalysis:

    def analyse(self, operation, weather_readings, date):
        if operation == 'e':
            return self.calculate_yearly_record(weather_readings, date.year)
        elif operation == 'a':
            return self.calculate_monthly_record(weather_readings, date)
        elif operation == 'c':
            return self.calculate_monthly_record_for_bar_charts(weather_readings, date)

    def update_yearly_highest_temp(self, report):
        max_temp_list = report['month_data'].attribute_values(
            'Max TemperatureC')
        year_max_temp = report['highest_temp']
        month_max_temp = max(list(filter(None, max_temp_list)))
        if year_max_temp <= month_max_temp:
            row = max_temp_list.index(month_max_temp)
            date_value = datetime.datetime.strptime(
                report['date_values'][row], '%Y-%m-%d')
            report['highest_temp'] = month_max_temp
            report['highest_temp_date'] = date_value

    def update_yearly_lowest_temp(self, report):
        min_temp_list = report['month_data'].attribute_values(
            'Min TemperatureC')
        month_min_temp = min(list(filter(None, min_temp_list)))
        year_min_temp = report['lowest_temp']
        if year_min_temp >= month_min_temp:
            row = min_temp_list.index(month_min_temp)
            date_value = datetime.datetime.strptime(
                report['date_values'][row], '%Y-%m-%d')
            report['lowest_temp'] = month_min_temp
            report['lowest_temp_date'] = date_value

    def update_yearly_most_humidity(self, report):
        highest_humidity_list = report['month_data'].attribute_values(
            'Max Humidity')
        year_highest_humidity = report['highest_humidity']
        month_highest_humid_day = max(
            list(filter(None, highest_humidity_list)))
        if year_highest_humidity <= month_highest_humid_day:
            row = highest_humidity_list.index(month_highest_humid_day)
            date_value = datetime.datetime.strptime(
                report['date_values'][row], '%Y-%m-%d')
            report['highest_humidity'] = month_highest_humid_day
            report['highest_humidity_date'] = date_value

    def calculate_yearly_record(self, weather_readings, year):
        months_data = weather_readings.months_data_of_year(year)
        report = {
            'highest_temp': float('-Inf'),
            'lowest_temp': float('Inf'),
            'highest_humidity': float('-Inf'),
        }
        for month in months_data:
            month_data = months_data.get(month)
            if not month_data:
                continue

            date_header = [header_value for header_value in month_data.csv_file_data.keys()
                           if 'PK' in header_value]
            date_values = month_data.csv_file_data.get(date_header[0])
            report['date_values'] = date_values
            report['month_data'] = month_data
            report['operation'] = 'e'
            self.update_yearly_highest_temp(report)
            self.update_yearly_lowest_temp(report)
            self.update_yearly_most_humidity(report)
        return report

    def calculate_monthly_record(self, weather_readings, date):
        months = weather_readings.months_data_of_year(date.year)
        report = {}
        month = months.get(calendar.month_name[date.month])
        if not month:
            return report

        max_temp_values = month.attribute_values(
            'Max TemperatureC')
        min_temp_values = month.attribute_values(
            'Min TemperatureC')
        mean_humidity_values = month.attribute_values(
            'Mean Humidity')
        max_temp_sum = sum(list(filter(None, max_temp_values)))
        min_temp_sum = sum(list(filter(None, min_temp_values)))
        mean_humidity_sum = sum(list(filter(None, mean_humidity_values)))
        total_max_temp_records = len(list(filter(None, max_temp_values)))
        total_min_temp_records = len(list(filter(None, min_temp_values)))
        total_mean_humidity_records = len(
            list(filter(None, mean_humidity_values)))
        report['operation'] = 'a'
        report['average_max_temp'] = (max_temp_sum / total_max_temp_records)
        report['average_min_temp'] = (min_temp_sum / total_min_temp_records)
        report['average_mean_humidity'] = (
            mean_humidity_sum / total_mean_humidity_records)
        return report

    def calculate_monthly_record_for_bar_charts(self, weather_readings, date):
        months_data = weather_readings.months_data_of_year(date.year)
        month_data = months_data.get(calendar.month_name[date.month])
        if not month_data:
            return {}

        date_header = [header_value for header_value in month_data.csv_file_data.keys()
                       if 'PK' in header_value]
        date_values = month_data.csv_file_data.get(date_header[0])
        report = {
            'operation': 'c',
            'high_temprature': month_data.attribute_values('Max TemperatureC'),
            'low_temprature': month_data.attribute_values('Min TemperatureC'),
            'dates': [datetime.datetime.strptime(date_value, '%Y-%m-%d')
                      for date_value in date_values]
        }
        return report
