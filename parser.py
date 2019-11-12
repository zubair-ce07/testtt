import sys
import os
from models import Weather
import calendar


class Parse:

    def __init__(self, date, data_files_list, path, info_type):
        weather_years = []
        # In this case, only year 1996 will be in date variable
        if info_type == '-e':
            files = [file_name for file_name in data_files_list if date in file_name]
        # In this case, year and month 1996/12 will be in date variable
        elif info_type == '-a' or info_type == '-c' or info_type == '-d':
            files = [file_name for file_name in data_files_list if calendar.month_name[int(date.split('/')[1])][0:3] in file_name and date.split('/')[0] in file_name]
        for file_name in files:
            with open(path+ "/" + file_name, 'r') as fp:
                line = fp.readline()
                cnt = 1
                while line:
                    if cnt >= 3 and '<!--' not in line:
                        weatherDetail = line.split(',')
                        weather = Weather()
                        weather.max_temprature = 0 if weatherDetail[1] == '' else int(weatherDetail[1])
                        weather.lowest_temprature = 0 if weatherDetail[3] == '' else int(weatherDetail[3])
                        weather.most_humid = 0 if weatherDetail[7] == '' else int(weatherDetail[7])
                        weather.date = weatherDetail[0]
                        weather_years.append(weather)
                    line = fp.readline()
                    cnt += 1
        self.data = weather_years
