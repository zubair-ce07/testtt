#!/usr/bin/python3.6

from constants import MONTHS_NAME
from csv_file_ds import Csv_file_ds

def calculate_yearly_record(years, current_year):
    highest_temp_struct, lowest_temp_struct, most_humid_struct, result = [], [], [], []
    year_max_temp, year_min_temp, year_highest_humidity = -273, 200, 0
    month_list = years.get_months_list_by_year(current_year)
    for month in month_list:
        if month is not None:
            max_temp_list = month.get_int_converted_attribute_values('Max TemperatureC')
            month_max_temp = max(list(filter(None.__ne__, max_temp_list)))
            if year_max_temp <= month_max_temp:
                highest_temp_struct = [month_max_temp, \
                    MONTHS_NAME[month_list.index(month)], \
                    max_temp_list.index(month_max_temp)+1]
                year_max_temp = month_max_temp
            min_temp_list = month.get_int_converted_attribute_values('Min TemperatureC')
            month_min_temp = min(list(filter(None.__ne__, min_temp_list)))
            if year_min_temp >= month_min_temp:
                lowest_temp_struct = [month_min_temp, \
                    MONTHS_NAME[month_list.index(month)], \
                    min_temp_list.index(month_min_temp)+1]
                year_min_temp = month_min_temp
            highest_humidity_list = month.get_int_converted_attribute_values('Max Humidity')
            month_highest_humid_day = max(list(filter(None.__ne__, highest_humidity_list)))
            if year_highest_humidity <= month_highest_humid_day:
                most_humid_struct = [month_highest_humid_day, \
                    MONTHS_NAME[month_list.index(month)], \
                    highest_humidity_list.index(month_highest_humid_day)+1]
                year_highest_humidity = month_highest_humid_day
            result = [highest_temp_struct, lowest_temp_struct, most_humid_struct]
    return result


def calculate_month_record(years, current_year, month_number):
    month_list = years.get_months_list_by_year(current_year)
    result = []
    month = month_list[month_number]
    if month is not None:
        max_temp_list = month.get_int_converted_attribute_values('Max TemperatureC')
        min_temp_list = month.get_int_converted_attribute_values('Min TemperatureC')
        mean_humidty_list = month.get_int_converted_attribute_values('Mean Humidity')

        result.append(sum(list(filter(None.__ne__, max_temp_list))) 
            /len(list(filter(None.__ne__, max_temp_list)))
            )

        result.append(sum(list(filter(None.__ne__, min_temp_list))) 
            /len(list(filter(None.__ne__, min_temp_list)))
            )

        result.append(sum(list(filter(None.__ne__, mean_humidty_list))) 
            /len(list(filter(None.__ne__, mean_humidty_list)))
            )    
    return result
    
def calculate_month_record_for_bar_charts(years, current_year, month_number):
    month_list = years.get_months_list_by_year(current_year)
    result = {}
    month = month_list[month_number]
    if month is not None:
        max_temp_list = month.get_int_converted_attribute_values('Max TemperatureC')
        min_temp_list = month.get_int_converted_attribute_values('Min TemperatureC')
        result['high_temprature'] = max_temp_list
        result['low_temprature'] = min_temp_list
    return result
    
