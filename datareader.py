""" This file contains the WeatherReader, Calculator
    and result classes, which are used to store data,
    calculate results, and store those results respectively

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""

import csv
from os import listdir
from os.path import isfile, join, exists
from datetime import datetime

month_trans_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar',
                    4: 'Apr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep',
                    10: 'Oct', 11: 'Nov', 12: 'Dec'}


class OneDayWeather:
    timestamp = ''
    max_temp = ''
    min_temp = ''
    max_humidity = ''
    mean_humidity = ''

    def __init__(self, reading):
        self.timestamp = reading.get('PKT')
        self.max_temp = reading.get('MaxTemp')
        self.min_temp = reading.get('MinTemp')
        self.max_humidity = reading.get('MaxHumidity')
        self.mean_humidity = reading.get('MeanHumidity')


class WeatherReader:
    data = []

    def __init__(self, directory, request):
        self.data = []
        if exists(directory):
            all_files = [f for f in listdir(directory)]
        else:
            print("Directory does not exists!")
            return None

        year_month = request.split('/')
        year = request.split('/')[0]
        month = 0
        month_files = []
        if int(year) > 1000 and int(year) < 9999:
            files = [x for x in all_files if year in x]
        else:
            self.data.append('year_error')
            return None

        if len(year_month) > 1:
            if request.split('/')[1]:
                month = int(request.split('/')[1])

        if month and month > 0 and month < 13:
            month_files = [x for x in files
                           if month_trans_dict.get(month) in x]
            files = month_files
        else:
            self.data.append('month_error')
            return None

        for file in files:
            with open(directory + '/' + file) as csvfile:
                readCSV = csv.DictReader(csvfile,
                                         delimiter=',',
                                         skipinitialspace=True)
                for each_day in readCSV:
                    req_attr = {'PKT': each_day.get('PKT'),
                                'MaxTemp': each_day.get('Max TemperatureC'),
                                'MinTemp': each_day.get('Min TemperatureC'),
                                'MaxHumidity': each_day.get('Max Humidity'),
                                'MeanHumidity': each_day.get('Mean Humidity')}

                    one_day_filtered_weather = OneDayWeather(req_attr)
                    self.data.append(one_day_filtered_weather)
