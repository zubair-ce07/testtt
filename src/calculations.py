#!/usr/bin/python3

import csv
from glob import glob

from data_holder import WeatherData


class WeatherCalculations:
    '''
    This class perform calculation to create weather report
    '''

    def highest_temp_record(self, data):
        '''
        This method takes list of WeatherData and return data having max_temp.
        '''
        return max(data, key=lambda day: day.max_temp)

    def lowest_temp_record(self, data):
        '''
        This method takes list of WeatherData and return data having min_temp.
        '''
        return min(data, key=lambda day: day.max_temp)

    def highest_humidity_record(self, data):
        '''
        This method takes list of WeatherData and return data having maximum
        mean_humidity.
        '''
        return max(data, key=lambda day: day.mean_humidity)

    def average_max_temp(self, data):
        '''
        This method take list of WeatherData and return mean of max_temp.
        '''
        max_temp_list = [day.max_temp for day in data]
        return sum(max_temp_list) // len(max_temp_list)

    def average_min_temp(self, data):
        '''
        This method take list of WeatherData and return mean of min_temp.
        '''
        min_temp_list = [day.min_temp for day in data]
        return sum(min_temp_list) // len(min_temp_list)

    def average_mean_humidity(self, data):
        '''
        This method take list of WeatherData and return mean of mean_humidity.
        '''
        mean_humdity_list = [day.mean_humidity for day in data]
        return sum(mean_humdity_list) // len(mean_humdity_list)

    def all_weather_record(self, dir_path):
        files_path = glob(f'{dir_path}*.txt')
        records = []
        for file_path in files_path:
            with open(file_path) as data_file:
                records += [WeatherData(row) for row in csv.DictReader(data_file) if self.validate_record(row)]
        return records

    def validate_record(self, record):
        required_data = [record.get('Max TemperatureC'),
                         record.get('Min TemperatureC'),
                         record.get(' Mean Humidity'),
                         record.get('PKT') or record.get('PKST')]
        if [x for x in required_data if not x]:
            return False
        return True

    def month_record(self, data_list, req_date):
        return [day for day in data_list if day.date.year == req_date.year and day.date.month == req_date.month]

    def year_record(self, data_list, req_date):
        return [day for day in data_list if day.date.year == req_date.year]

    def extreme_record(self, data):
        return self.highest_temp_record(data), self.lowest_temp_record(data), self.highest_humidity_record(data)

    def average_values(self, data):
        return self.average_max_temp(data), self.average_min_temp(data), self.average_mean_humidity(data)
