import os.path
import calendar
import csv
from WeatherReport import *
from WeatherAnalyzer import *

class Weather:

    def __init__(self):
        self.weather_analyzer = WeatherAnalyzer()

    def read_weather_file(self,filepath):
        if os.path.exists(filepath):
            with open (filepath) as weatherfile:
                reader = csv.DictReader(weatherfile)
                weather_readings = [tuple((row['PKT'],row['Max TemperatureC'],row['Min TemperatureC'], \
                                    row['Max Humidity'],row[' Mean Humidity'])) for row in reader if \
                                    row['Max TemperatureC'] is not '' and row['Min TemperatureC'] is not \
                                    '' and row['Max Humidity'] is not '' and row[' Mean Humidity'] is not '']
            return weather_readings
        else:
            return False

    def get_formatted_date(self,date):
        segmented_date = date.split('-')
        return f'{calendar.month_name[int(segmented_date[1])]} {segmented_date[2]}'

class YearlyWeather(Weather):

    def __init__(self,filenames):
        Weather.__init__(self)
        self.filenames = filenames

    def read_yearly_weather(self):
        yearly_weather = False
        for month_wise_files_counter in self.filenames:
            weather_record = self.read_weather_file(month_wise_files_counter)
            if weather_record:
                self.weather_analyzer.initialize_yearly_weather(weather_record)
                yearly_weather = True
        return yearly_weather

    def __str__(self):
        return (f'Highest Temperature: {self.weather_analyzer.yearly_highest_temperature}C on '+
                f'{self.get_formatted_date(self.weather_analyzer.yearly_hightest_temperature_date)}'+
                f'\nLowest Temperature: {self.weather_analyzer.yearly_lowest_temperature}C on '+
                f'{self.get_formatted_date(self.weather_analyzer.yearly_lowest_temperature_date)}'+
                f'\nHighest Humidity: {self.weather_analyzer.yearly_highest_humidity}% on '+
                f'{self.get_formatted_date(self.weather_analyzer.yearly_highest_humidity_date)}')


class MonthlyWeather(Weather):

    def __init__(self,filepath):
        Weather.__init__(self)
        self.filepath = filepath

    def read_monthly_weather(self):
        weather_record = self.read_weather_file(self.filepath)
        if weather_record:
            self.weather_analyzer.initialize_monthly_weather(weather_record)
            return True
        else:
            return False

    def read_daily_weather(self):
        monthly_max_readings = self.weather_analyzer.max_temperature_per_day
        monthly_min_readings = self.weather_analyzer.min_temperature_per_day

        for index,value in enumerate (monthly_max_readings):
            weather_graph = WeatherReport(monthly_max_readings[index],monthly_min_readings[index])
            print('\033[91m'+str(index+1),end='')
            weather_graph.max_temperature_graph(str(index+1))
            print ('\033[91m'+'('+str(monthly_max_readings[index])+')')
            print('\033[94m'+str(index+1),end='')
            weather_graph.min_temperature_graph(str(index+1))
            print ('\033[94m'+'('+str(monthly_min_readings[index])+')')

    def analyze_daily_graph_weather(self):
        monthly_max_readings = self.weather_analyzer.max_temperature_per_day
        monthly_min_readings = self.weather_analyzer.min_temperature_per_day

        for index,value in enumerate (monthly_max_readings):
            weather_graph = WeatherReport(monthly_max_readings[index],monthly_min_readings[index])
            weather_graph.merged_graph(str(index+1))

    def __str__(self):
        return f'Highest Average: {self.weather_analyzer.monthly_highest_average}C\
                 \nLowest Average: {self.weather_analyzer.monthly_lowest_average}C\
                 \nAverage Mean Humidity: {self.weather_analyzer.monthly_average_mean_humidity}%'
