#!/usr/bin/python3.6

import csv
import sys
import re

import calculations
import constants

from weather_man_ds import Weather_man_ds
from read_csv_file import read_csv_file
from result_generation import display_results

# for iterating cmd line arguments
argv_index = 2
# main function
if len(sys.argv) % 2 == 0 and len(sys.argv) >= 4:
    years = Weather_man_ds()
    files_path = sys.argv[1]
    if files_path[-1] != '/':
        files_path = files_path + '/'
    while(argv_index < len(sys.argv)):
        current_operation = sys.argv[argv_index] + sys.argv[argv_index+1]
        current_year = sys.argv[argv_index+1][:4]
        month_list = years.get_months_list_by_year(current_year)
        if month_list is None:
            month_list = []
            for name in constants.MONTHS_NAME:
                file_path = files_path + 'Murree_weather_' + current_year + '_' + name[:3] + '.txt'
                my_month = read_csv_file(file_path)
                month_list.append(my_month)
            years.add_new_year(current_year, month_list)
        if re.match(r'-e\d{4}$', current_operation):
            result = calculations.calculate_yearly_record(years, current_year)
            result.append(current_year)
            display_results(result, current_operation[1])
        elif re.match(r'-[ac]\d{4}/0?[1-9]|[1-9][0-2]$', current_operation):
            month_number = int(sys.argv[argv_index+1][sys.argv[argv_index+1].find('/')+1:])-1
            if current_operation[1] == 'a':
                result = calculations.calculate_month_record(
                    years, current_year, month_number
                    )
                result.append(constants.MONTHS_NAME[month_number] + ', ' + current_year)
            else:
                result = calculations.calculate_month_record_for_bar_charts(
                    years, current_year, month_number)
                result['year'] = (constants.MONTHS_NAME[month_number] + ', ' + current_year)
            display_results(result, current_operation[1])
        else:
            print(constants.ARGUMENT_ERROR_MESSAGE, current_operation)
        argv_index += 2