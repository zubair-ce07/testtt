__author__ = 'mazharshah'
# __author__ = 'mazharshah'
import os
import csv

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
    for element in max_min_Data:
        print('\t\t\t\t'.join([str(x) for x in element]))


# First of All Take input from user ..
print ' For Annual Max_Min Temperature Press 1\n' \
      ' For Hottest Day of Each year Press 2\n' \
      ' For Coldest day of Each year Press 3'

report_no = input('Enter Report No: ')


if report_no == int and report_no in [1, 2, 3]:
    print 'No is : ', report_no

# Picking all the names of files in a directory
files_list = sorted(os.listdir("weatherdata/"))

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
    #           Else Part
    # ======================================================#

    file_path = 'weatherdata/' + file_name

    with open(file_path) as f:
        lines = f.readlines()[1:-1]

        file_dict = csv.DictReader(lines)

        for day_row in file_dict:
            # print day_row#["PKT"]

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


if report_no == 1:
    print display_Max_Min_info(max_min_Data)
elif report_no == 2:
        print display_hottest_day_info(hot_day_data)
elif report_no == 3:
    print display_coldest_day_info(cold_day_data)
else:
    "Wrong Input!!"