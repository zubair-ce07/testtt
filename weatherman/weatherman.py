import os
import argparse


def max_temp_func(new_temp, old_temp, new_date, old_date):
    if new_temp > old_temp:
        return new_temp, new_date
    else:
        return old_temp, old_date


def min_temp_func(new_temp, old_temp):
    if new_temp < old_temp:
        return new_temp
    else:
        return old_temp


def max_humid_func(new_humid, old_humid):
    if new_humid > old_humid:
        return new_humid
    else:
        return old_humid


def min_humid_func(new_humid, old_humid):
    if new_humid < old_humid:
        return new_humid
    else:
        return old_humid


def reset_val_func():
    return 0, 0, '0', 1000, 1000


def main():
    data_dir = '/home/sulman/Downloads/weatherdata'
    report_no = 2

    status = 'not working'

    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year = [1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011]

    if os.path.isdir(data_dir):
        status = 'working'

        if report_no is 1:
            print('\033[1m' + '\n1. Annual Max/Min Temp:\n' + '\033[0m')
            print('\tYear\tMax Temp\tMin Temp\tMax Humidity\tMin Humidity\n\t' + '-' * 68)

            month_count = 0
            year_count = 0

            max_temp, max_humid, useless, min_temp, min_humid, = reset_val_func()

            while year_count < 16:

                if month_count < 12:

                    if not os.path.isfile('{}/lahore_weather_{}_{}.txt'.format(data_dir, year[year_count], month[month_count])):
                        month_count += 1
                        continue

                    f = open('{}/lahore_weather_{}_{}.txt'.format(data_dir, year[year_count], month[month_count]), 'r')

                    for i, line in enumerate(f):
                        arr_line = [x for x in line.split(',')]

                        if arr_line[0][0].isdigit():

                            if arr_line[1].isdigit():
                                max_temp, useless = max_temp_func(int(arr_line[1]), max_temp, useless, useless)

                            if arr_line[3].isdigit():
                                min_temp = min_temp_func(int(arr_line[3]), min_temp)

                            if arr_line[7].isdigit():
                                max_humid = max_humid_func(int(arr_line[7]), max_humid)

                            if arr_line[9].isdigit():
                                min_humid = min_humid_func(int(arr_line[9]), min_humid)

                    month_count += 1
                    f.close()

                if month_count > 11:
                    print('\t{}\t{}\t\t{}\t\t{}\t\t{}'.format(year[year_count], max_temp, min_temp, max_humid,
                                                              min_humid))
                    month_count = 0
                    year_count += 1
                    max_temp, max_humid, useless, min_temp, min_humid, = reset_val_func()

        elif report_no is 2:
            print('\033[1m' + '\n2. Hottest day of each year\n' + '\033[0m')
            print('\tYear\tDate\t\tTemp\n\t' + '-' * 28)

            month_count = 0
            year_count = 0

            max_temp, useless, date, useless, useless = reset_val_func()

            while year_count < 14:

                if month_count < 12:

                    if not os.path.isfile('{}/lahore_weather_{}_{}.txt'.format(data_dir, year[year_count], month[month_count])):
                        month_count += 1
                        continue

                    f = open("{}/lahore_weather_{}_{}.txt".format(data_dir, year[year_count], month[month_count]), 'r')

                    for i, line in enumerate(f):
                        arr_line = [x for x in line.split(',')]

                        if arr_line[0][0].isdigit():

                            if arr_line[1].isdigit():
                                max_temp, date = max_temp_func(int(arr_line[1]), max_temp, arr_line[0], date)

                    month_count += 1
                    f.close()

                if month_count > 11:
                    format_date = [x for x in date.split('-')]
                    print('\t{}\t{}/{}/{}\t{}'.format(year[year_count], format_date[2], format_date[1], format_date[0],
                                                      max_temp))
                    month_count = 0
                    year_count += 1
                    max_temp, useless, date, useless, useless = reset_val_func()

    if status == 'not working' or report_no not in (1,2):
        print("Usage: weatherman\n<report#>\n<data_dir>\n\n[Report #]\n1 for Annual Max/Min Temperature\n"
              "2 for Hottest day of each year\n3 for coldest day of each year\n\n[data_dir]\n"
              "Directory containing weather data files\n")


if __name__ == "__main__":
    main()
