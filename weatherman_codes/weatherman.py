""" Weatherman program driver file

It should be run from terminal with arguments of following types:
1. weatherman.py -e 2002 ../weatherdata
2. weatherman.py -a 2005/6 ../weatherdata
3. weatherman.py -c 20011/3 ../weatherdata

1st will display given year's highlights
2nd will display given month's average
3rd will display bar charts for whole month

Pylint Score: 6.55
All objections are on my variables, pylint consider them constants
"""

import sys
import csv
from constants import MONTHS
from functions import get_day, get_month, get_average, locate

action = sys.argv[1]
period = sys.argv[2]
path = sys.argv[3]

# First to check if the arguments are complete i.e 4 or not
if len(sys.argv) != 4:
    print('Invalid Arguments')
    print('There should be 4 arguments:',
          'file.py [-a|-c|-e] [year|year/month] path/to/weatherdata/folder')

else:
    if action == '-a' or action == '-c':
        # When we need to work on one file only
        if (len(period) == 6 or len(period) == 7) and period[4] == '/':
            # When correct input in year/month style
            year = period[:4]
            month_no = int(period[5:])
            month = MONTHS[month_no]

            if 1996 <= int(year) <= 2011:
                # correct year
                if 0 < month_no <= 12:
                    # correct month
                    print(month, year)
                    if year == '1996' and month_no != 12:
                        # We have only december data for year 1996
                        print('No record for this month in 1996, only December\'s available')
                    else:
                        # When file exist for given input

                        mon = '{:.3}'.format(month)
                        cur_path = '{}/lahore_weather_{}_{}.txt'.format(path, year, mon)
                        data = []

                        with open(cur_path, 'r') as read_file:
                            reader = csv.reader(read_file)
                            for row in reader:
                                data.append(row)

                        head_row = 0
                        max_temp_col = 0
                        min_temp_col = 0
                        mean_humid_col = 0
                        day_col = 0

                        # finding header row and the required columns
                        locations = locate(data)
                        head_row = locations[0]
                        time_col = locations[1]
                        max_temp_col = locations[2]
                        min_temp_col = locations[3]
                        mean_humid_col = locations[5]

                        total_no = len(data) - head_row - 2

                        if action == '-a':
                            # Average of data should be returned

                            avg_max_temp = get_average(data, head_row, max_temp_col, total_no)
                            avg_min_temp = get_average(data, head_row, min_temp_col, total_no)
                            avg_mean_humid = get_average(data, head_row, mean_humid_col, total_no)
                            print('Highest Average: {}C'.format(avg_max_temp))
                            print('Lowest Average: {}C'.format(avg_min_temp))
                            print('Average Humidity: {}%'.format(avg_mean_humid))

                        elif action == '-c':
                            # Bar charts of daily data should be returned

                            for k in range(head_row + 1, len(data) - 1):
                                day = get_day(data[k][day_col])
                                if data[k][min_temp_col] != '':
                                    min_temp = data[k][min_temp_col]
                                    min_temp_bar = '\033[1;34m{}\033[1;m'.format('+' * int(min_temp))
                                if data[k][max_temp_col] != '':
                                    max_temp = data[k][max_temp_col]
                                    max_temp_bar = '\033[1;31m{}\033[1;m'.format('+' * int(max_temp))

                                if data[k][min_temp_col] != '':
                                    if data[k][max_temp_col] != '':
                                        print('{} {}{} {}C - {}C'
                                              .format(day, min_temp_bar, max_temp_bar,
                                                      min_temp, max_temp))
                                    else:
                                        print('{} {} {}C'.format(day, min_temp_bar, min_temp))
                                elif data[k][max_temp_col] != '':
                                    print('{} {} {}C'.format(day, max_temp_bar, max_temp))
                                else:
                                    print('{} No Data'.format(day))

                else:
                    # wrong month
                    print('Month should be any from 1 to 12')

            else:
                # wrong year
                print('Year should be any from 1996 to 2011')

        else:
            # wrong 3rd input
            print('Invalid Arguments')
            print('3rd argument should be in year/month format (e.g: 2001/3)',
                  'and year should be any from 1996 to 2011')

    elif action == '-e':
        # When we have to work on all files of a year

        if len(period) == 4 and 1996 <= int(period) <= 2011:
            # valid year input
            year = period

            max_temp = 0
            min_temp = 100
            max_humid = 0
            max_temp_date = ''
            min_temp_date = ''
            max_humid_date = ''

            if year == '1996':
                # becoz we have only 1 month data for 1996
                cur_path = '{}/lahore_weather_{}_Dec.txt'.format(path, year)
                data = []

                # read file
                with open(cur_path, 'r') as read_file:
                    reader = csv.reader(read_file)
                    for row in reader:
                        data.append(row)

                head_row = 0
                max_temp_col = 0
                min_temp_col = 0
                max_humid_col = 0
                day_col = 0

                # finding header row and the required columns
                locations = locate(data)
                head_row = locations[0]
                time_col = locations[1]
                max_temp_col = locations[2]
                min_temp_col = locations[3]
                max_humid_col = locations[4]

                # getting required data
                for k in range(head_row + 1, len(data) - 1):
                    if data[k][max_temp_col] != '':
                        if int(data[k][max_temp_col]) > max_temp:
                            max_temp = int(data[k][max_temp_col])
                            max_temp_date = data[k][day_col]
                    if data[k][min_temp_col] != '':
                        if int(data[k][min_temp_col]) < min_temp:
                            min_temp = int(data[k][min_temp_col])
                            min_temp_date = data[k][day_col]
                    if data[k][max_humid_col] != '':
                        if int(data[k][max_humid_col]) > max_humid:
                            max_humid = int(data[k][max_humid_col])
                            max_humid_date = data[k][day_col]

            else:
                # for other years, we have to process all 12 months files
                for n in MONTHS:
                    mon = '{:.3}'.format(MONTHS[n])
                    cur_path = '{}/lahore_weather_{}_{}.txt'.format(path, year, mon)
                    data = []

                    # read file
                    with open(cur_path, 'r') as read_file:
                        reader = csv.reader(read_file)
                        for row in reader:
                            data.append(row)

                    head_row = 0
                    max_temp_col = 0
                    min_temp_col = 0
                    max_humid_col = 0
                    day_col = 0

                    # finding header row and the required columns
                    locations = locate(data)
                    head_row = locations[0]
                    time_col = locations[1]
                    max_temp_col = locations[2]
                    min_temp_col = locations[3]
                    max_humid_col = locations[4]

                    # getting required data
                    for k in range(head_row + 1, len(data) - 1):
                        if data[k][max_temp_col] != '':
                            if int(data[k][max_temp_col]) > max_temp:
                                max_temp = int(data[k][max_temp_col])
                                max_temp_date = data[k][day_col]
                        if data[k][min_temp_col] != '':
                            if int(data[k][min_temp_col]) < min_temp:
                                min_temp = int(data[k][min_temp_col])
                                min_temp_date = data[k][day_col]
                        if data[k][max_humid_col] != '':
                            if int(data[k][max_humid_col]) > max_humid:
                                max_humid = int(data[k][max_humid_col])
                                max_humid_date = data[k][day_col]

            max_temp_month = get_month(max_temp_date)
            max_temp_day = get_day(max_temp_date)
            min_temp_month = get_month(min_temp_date)
            min_temp_day = get_day(min_temp_date)
            max_humid_month = get_month(max_humid_date)
            max_humid_day = get_day(max_humid_date)

            print('Highest: {}C on {} {}'.format(max_temp, max_temp_month, max_temp_day))
            print('Lowest: {}C on {} {}'.format(min_temp, min_temp_month, min_temp_day))
            print('Humid: {}% on {} {}'.format(max_humid, max_humid_month, max_humid_day))

        else:
            # wrong 3rd input
            print('3rd argument should be any 4-digit year from 1996 to 2011')

    else:
        # wrong 2nd input
        print('Invalid Arguments')
        print('2nd argument should be either -a, -c or -e')
