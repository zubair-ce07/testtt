""" This file contains the WeatherReader, Calculator
    and result classes, which are used to store data,
    calculate results, and store those results respectively

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""

import csv
from os import listdir

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

    def __init__(self, directory, year, month):
        self.data = []
        all_files = [f for f in listdir(directory)]
        files = [x for x in all_files if year in x]

        if month:
            month_files = [x for x in files
                           if month_trans_dict.get(int(month)) in x]
            files = month_files

        for file in files:
            with open(directory + '/' + file) as csvfile:
                file_read_as_csv = csv.DictReader(csvfile,
                                                  delimiter=',',
                                                  skipinitialspace=True)
                for each_day in file_read_as_csv:
                    req_attr = {'PKT': each_day.get('PKT'),
                                'MaxTemp': each_day.get('Max TemperatureC'),
                                'MinTemp': each_day.get('Min TemperatureC'),
                                'MaxHumidity': each_day.get('Max Humidity'),
                                'MeanHumidity': each_day.get('Mean Humidity')}

                    one_day_filtered_weather = OneDayWeather(req_attr)
                    self.data.append(one_day_filtered_weather)
