import os.path
import calendar
from weatherReport import *
from weatherData import *
from collections import namedtuple

class Weather:

    def __init__(self):
        self.weather_data = weatherData();

    def read_weather_file(self,filepath):
        weather_readings = []
        if os.path.exists(filepath):
            with open(filepath) as weather_details:
                next(weather_details)
                for line in weather_details:
                    weather_parameters = line.split(',')
                    if weather_parameters[1] is not '' and weather_parameters[3] is not '' and weather_parameters[7] is not '' and weather_parameters[8] is not '':
                        weather_readings.append(tuple((weather_parameters[0],weather_parameters[1],weather_parameters[3],weather_parameters[7],weather_parameters[8])))
            weather_details.close()
            return weather_readings
        else:
            return -1

    def get_formatted_date(self,date):
        segmented_date = date.split('-')
        formatted_date = calendar.month_name[int(segmented_date[1])-1]+' '+segmented_date[2]
        return formatted_date


class YearlyWeather(Weather):

    def __init__(self,filenames):
        Weather.__init__(self)
        self.filenames = filenames

    def verify_yearly_data(self):
        file_found = False
        for file_count in self.filenames:
            if os.path.exists(file_count):
                return True

        return False

    def get_yearly_weather(self):
        for month_wise_files_counter in self.filenames:
            weather_data = self.read_weather_file(month_wise_files_counter)
            if weather_data != -1:
                self.weather_data.initialize_yearly_data(weather_data)
        return self.weather_data.get_yearly_weather_details()

    def __str__(self):
          yearly_weather_details = self.weather_data.get_yearly_weather_details()
          result = 'Highest Temperature: %sC on %s'%(yearly_weather_details['highest_annual_temperature'],self.get_formatted_date(yearly_weather_details['highest_annual_temperature_date'])) + '\n'
          result += 'Lowest Temperature: %sC on %s'%(yearly_weather_details['lowest_annual_temperature'],self.get_formatted_date(yearly_weather_details['lowest_annual_temperature_date']))  + '\n'
          result += 'Highest Humidity: %s%% on %s'%(yearly_weather_details['highest_annual_humidity'],self.get_formatted_date(yearly_weather_details['highest_annual_humidity_date']))
          return result


class MonthlyWeather(Weather):

    def __init__(self,filepath):
        Weather.__init__(self)
        self.filepath = filepath
        weather_data = self.read_weather_file(self.filepath)
        if weather_data != -1:
            self.weather_data.initialize_monthly_data(self.read_weather_file(self.filepath))

    def verify_monthly_data(self):
        file_found = False

        if os.path.exists(self.filepath):
            file_found = True

        return file_found

    def get_monthly_weather(self):
        return self.weather_data.get_monthly_weather_details()

    def get_daily_temperature(self):
        monthly_max_readings = self.weather_data.get_monthly_max_readings()
        monthly_min_readings = self.weather_data.get_monthly_min_readings()

        for index,value in enumerate (monthly_max_readings):
            weather_graph = WeatherReport(monthly_max_readings[index],monthly_min_readings[index])
            print('\033[91m'+str(index+1),end='')
            weather_graph.max_temperature_graph(str(index+1))
            print ('\033[91m'+'('+str(monthly_max_readings[index])+')')
            print('\033[94m'+str(index+1),end='')
            weather_graph.min_temperature_graph(str(index+1))
            print ('\033[94m'+'('+str(monthly_min_readings[index])+')')

    def read_data_for_daily_graph(self):
        monthly_max_readings = self.weather_data.get_monthly_max_readings()
        monthly_min_readings = self.weather_data.get_monthly_min_readings()

        for index,value in enumerate (monthly_max_readings):
            weather_graph = WeatherReport(monthly_max_readings[index],monthly_min_readings[index])
            weather_graph.merged_graph(str(index+1))

    def __str__(self):
        monthly_weather_details = self.weather_data.get_monthly_weather_details()
        result = 'Highest Average: %sC'%(monthly_weather_details['monthly_highest_average']) + '\n'
        result += 'Lowest Average: %sC'%(monthly_weather_details['monthly_lowest_average']) + '\n'
        result += 'Average Mean Humidity: %s%%'%(monthly_weather_details['monthly_average_mean_humidity'])
        return result
