__author__ = 'mazharshah'
# __author__ = 'mazharshah'
#!/usr/bin/python

import os
import csv
import sys
import argparse

from enum import Enum


class ReportNo(Enum):

    annual_temp_humidity = 1
    annual_hottest_day = 2
    annual_coldest_day = 3


def display_hottest_day_info(info):
    print('\nHottest day of each year:\n')
    headings = ['Year', 'Date', 'Temp']
    print('\t\t\t'.join([str(x) for x in headings]))
    print('--'*19)

    for element in info:
        print('\t\t\t'.join([str(v) for v in element]))


def display_coldest_day_info(info):
    print('\nColdest day of each year:\n')
    headings = ['Year', 'Date', 'Temp']
    print('\t\t\t'.join([str(x) for x in headings]))
    print('--'*19)

    for element in info:
        print('\t\t\t'.join([str(v) for v in element]))


def display_Max_Min_info(info):
    headings = ['Year', 'MAX Temp', 'MIN Temp', 'MAX Humidity', 'Min Humidity']
    print('\t\t'.join([str(x) for x in headings]))
    print '--' * 38
    for element in info:
        print('\t\t\t'.join([str(x) for x in element]))

# #################################### MAIN #############################################

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("report_no", type=int)
    parser.add_argument("data_dir")
    args = parser.parse_args()

    report_no = args.report_no
    data_dir = args.data_dir

    if not os.path.exists(data_dir):
        print("Directory Not Found! : " + data_dir)
        sys.exit()

    # Picking all the names of files in a directory
    files_list = sorted(os.listdir(data_dir))

    max_min_Data = []
    hot_day_data = []
    cold_day_data = []

    # Fetching year from first file
    year = int(files_list[0][-12:-8])

    max_temp_c = -1000
    max_temp_day = None

    min_temp_c = 1000
    min_temp_day = None

    max_humidity = -1000
    min_humidity = 1000

    for file_name in files_list:

        year_month = file_name[:-4][-8:].split("_")

        if int(year) < int(year_month[0]):
            # Making one Row of a result! i.e. for Max-Min Temperature
            yearlyData = [
                year, max_temp_c,
                min_temp_c,
                max_humidity,
                min_humidity
            ]

            # This is the ROW of Hottest day table
            hot_day_info = [
                year,
                max_temp_day,
                max_temp_c
            ]

            # This is the Row of Coldest Day table
            cold_day_info = [
                year,
                min_temp_day,
                min_temp_c
            ]

            # Contains every year's Max-Min Temperature
            max_min_Data.append(yearlyData)

            # Contains Every year's Hottest day and Temp
            hot_day_data.append(hot_day_info)

            # Contains Every year's Coldest day and Temp
            cold_day_data.append(cold_day_info)

            # Re-Initializing variables
            max_temp_c = -1000
            max_temp_day = None

            min_temp_c = 1000
            min_temp_day = None

            max_humidity = -1000
            min_humidity = 1000

            year = year_month[0]

        # ======================================================#
        #           Below Code will always Run 'Not ELSE'
        # ======================================================#

        # If block for making a path e.g weather_data -> weather_data/
        if not str(args.data_dir)[-1].__eq__('/'):
            data_dir = args.data_dir + '/'

        file_path = data_dir + file_name

        with open(file_path) as f:
            lines = f.readlines()[1:-1]

            file_dict = csv.DictReader(lines)

            for day_row in file_dict:

                day_temperature = day_row['Max TemperatureC']

                if day_temperature is not '':
                    if int(day_temperature) > int(max_temp_c):
                        try:
                            max_temp_day = day_row['PKT']
                        except KeyError:
                            max_temp_day = day_row['PKST']
                        max_temp_c = day_temperature

                day_temperature = day_row['Min TemperatureC']
                if day_temperature is not '':
                    if int(day_temperature) < int(min_temp_c):
                        try:
                            min_temp_day = day_row['PKT']
                        except KeyError:
                            min_temp_day = day_row['PKST']

                        min_temp_c = day_temperature

                day_humidity = day_row['Max Humidity']
                if day_humidity is not '':
                    if int(day_humidity) > int(max_humidity):
                        max_humidity = day_humidity

                day_humidity = day_row[' Min Humidity']
                if day_humidity is not '':
                    if int(day_humidity) < int(min_humidity):
                        max_humidity = day_humidity
    if report_no == ReportNo.annual_temp_humidity.value:
        print display_Max_Min_info(max_min_Data)

    elif report_no == ReportNo.annual_hottest_day.value:
            print display_hottest_day_info(hot_day_data)

    elif report_no == ReportNo.annual_coldest_day.value:
        print display_coldest_day_info(cold_day_data)

    else:
        print('Usage:\tweatherman <report#> <directory path> ')
        sys.exit(2)


if __name__ == "__main__":
    main()