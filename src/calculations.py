#!/usr/bin/python3
import datetime
import csv


class WeatherCalculations:
    '''
    This class perform calculation to create weather report
    '''

    def highest_temparature_record(self, year_data):
        '''
        This method takes list of WeatherData and return data having max_temp.
        '''
        max_temp_record = sorted(
            year_data, key=lambda day: day.max_temp, reverse=True)[0]
        return max_temp_record

    def lowest_temparature_recored(self, year_data):
        '''
        This method takes list of WeatherData and return data having min_temp.
        '''
        min_temp_record = sorted(
            year_data, key=lambda day: day.max_temp, reverse=False)[0]
        return min_temp_record

    def highest_humidity_recored(self, year_data):
        '''
        This method takes list of WeatherData and return data having maximum
        mean_humidity.
        '''
        max_humid_record = sorted(
            year_data, key=lambda day: day.mean_humidity, reverse=True)[0]
        return max_humid_record

    def average_max_temp(self, month_data):
        '''
        This method take list of WeatherData and return mean of max_temp.
        '''
        max_temp_list = [day.max_temp for day in month_data]
        mean = sum(max_temp_list) / len(max_temp_list)
        return int(round(mean, 0))

    def average_min_temp(self, month_data):
        '''
        This method take list of WeatherData and return mean of min_temp.
        '''
        min_temp_list = [day.min_temp for day in month_data]
        mean = sum(min_temp_list) / len(min_temp_list)
        return int(round(mean, 0))

    def average_mean_humidity(self, month_data):
        '''
        This method take list of WeatherData and return mean of mean_humidity.
        '''
        mean_humdity_list = [day.mean_humidity for day in month_data]
        mean = sum(mean_humdity_list) / len(mean_humdity_list)
        return int(round(mean, 0))
