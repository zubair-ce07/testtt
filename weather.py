import os
import csv
from datetime import datetime


class WeatherReader:
    def read_weather_rows(self, files_path):
        weather_files = os.listdir(files_path)
        weather_rows = []
        for weather_file in weather_files:
            file_name = os.path.join(files_path, weather_file)
            with open(file_name) as f_obj:
                reader = csv.DictReader(f_obj)
                weather_rows += list(reader)
        return weather_rows

    def filter_rows_according_pattern(self, weather_rows, pattern):
        return [row for row in weather_rows if pattern in row.get('PKT', row.get('PKST'))]


class WeatherCalculator:
    def extract_weather_attribute(self, weather_readings, attribute_key):
        weather_attribute_readings = []
        for day_weather in weather_readings:
            day = day_weather.get('PKT', day_weather.get('PKST'))
            day = datetime.strptime(day, '%Y-%m-%d')
            column_with_date = {
                'day': day,
                attribute_key: day_weather.get(attribute_key)
            }
            weather_attribute_readings.append(column_with_date)
        return weather_attribute_readings

    def show_calculations(self, calc_display_format, attribute, day=None):
        if day:
            print(calc_display_format.format(attribute, day.strftime('%B'), day.day))
        else:
            print(calc_display_format.format(attribute))

    def calculate_average(self, attribute_readings):
        average = sum(attribute_readings) / len(attribute_readings)
        average = {'avrg': '{0:.2f}'.format(average)}
        return average

    def show_daily_extreme_temp(self, month_weather):
        max_temp_readings = self.extract_weather_attribute(month_weather, 'Max TemperatureC')
        min_temp_readings = self.extract_weather_attribute(month_weather, 'Min TemperatureC')
        for max_temp, min_temp in zip(max_temp_readings, min_temp_readings):
            day = min_temp.get('day')
            min_temp = min_temp.get('Min TemperatureC')
            max_temp = max_temp.get('Max TemperatureC')
            min_temp_bar = ''  # A bar containing min_temp_times '+' symbol in blue color
            max_temp_bar = ''  # A bar containing max_temp_times '+' symbol in red color
            if min_temp:
                min_temp_bar = '\033[94m+\033[0m' * int(min_temp)
                min_temp = min_temp + 'C-'
            if max_temp:
                max_temp_bar = '\033[95m+\033[0m' * int(max_temp)
                max_temp = max_temp + 'C'
            print('{} {}{} {}{}'.format(day.day, min_temp_bar, max_temp_bar, min_temp, max_temp))
        print('\nThe End')
