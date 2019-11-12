"""
This file contains file data parsing code
"""
import calendar
from models import Weather


class Parse:
    """
    Class for parsing weather file records
    """

    def __init__(self, date, data_files_list, path, info_type):
        weather_years = []
        # In this case, only year 1996 will be in date variable
        if info_type in '-e':
            files = [file_name for file_name in data_files_list if date in file_name]
        # In this case, year and month 1996/12 will be in date variable
        elif info_type in '-a' or info_type in '-c' or info_type in '-d':
            files = [file_name \
                for file_name \
                in data_files_list \
                    if calendar.month_name[\
                        int(date.split('/')[1])][0:3] \
                            in file_name \
                                and date.split('/')[0] in file_name]
        for file_name in files:
            with open(path+ "/" + file_name, 'r') as file_path:
                line = file_path.readline()
                cnt = 1
                while line:
                    if cnt >= 3 and '<!--' not in line:
                        weather_detail = line.split(',')
                        weather = Weather()
                        weather.max_temprature = 0 \
                            if weather_detail[1] == '' \
                                else int(weather_detail[1])
                        weather.lowest_temprature = 0 \
                            if weather_detail[3] == '' \
                                else int(weather_detail[3])
                        weather.most_humid = 0 \
                            if weather_detail[7] == '' \
                                else int(weather_detail[7])
                        weather.date = weather_detail[0]
                        weather_years.append(weather)
                    line = file_path.readline()
                    cnt += 1
        self.data = weather_years
