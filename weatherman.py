import argparse
import sys
import os
import statistics

import report_generator

PKT, PKT_INDEX = 'PKT', 0
MAX_TEMP, MAX_TEMP_INDEX = 'Max Temp', 1
MEAN_TEMP, MEAN_TEMP_INDEX = 'Mean Temp', 2
MIN_TEMP, MIN_TEMP_INDEX = 'Min Temp', 3
MEAN_HUMIDITY, MEAN_HUMIDITY_INDEX = 'Mean Humidity', 8

MONTHS_ABBREVIATED = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                      ]

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December'
          ]


# class DayInfo:
#     def __init__(self, info):
#         self.pkt = info[0] if info[0] != '' else None
#         self.max_temp = int(info[1]) if info[1] != '' else None
#         self.mean_temp = int(info[2]) if info[2] != '' else None
#         self.min_temp = int(info[3]) if info[3] != '' else None
#         self.mean_humidity = int(info[8]) if info[8] != '' else None
#
#
# def parse(files_dir, files):
#     weather_readings = []
#
#     for file in files:
#         with open(files_dir + file) as f:
#             next(f)
#
#             # line contains information of a single day of a month
#             for line in f:
#                 line = line.strip().split(',')
#                 weather_readings.append(DayInfo(line))
#
#     return weather_readings


def parse(files_dir, file_names):
    weather_readings = {PKT: [], MAX_TEMP: [], MEAN_TEMP: [],
                        MIN_TEMP: [], MEAN_HUMIDITY: []
                        }
    for file in file_names:
        with open(files_dir + file) as f:
            next(f)

            # info contains information of a single day of a month
            for info in f:
                info = info.strip().split(',')
                weather_readings[PKT].append(info[PKT_INDEX])
                weather_readings[MAX_TEMP].append(int(info[MAX_TEMP_INDEX]) if info[MAX_TEMP_INDEX] != '' else None)
                weather_readings[MEAN_TEMP].append(int(info[MEAN_TEMP_INDEX]) if info[MEAN_TEMP_INDEX] != '' else None)
                weather_readings[MIN_TEMP].append(int(info[MIN_TEMP_INDEX]) if info[MIN_TEMP_INDEX] != '' else None)
                weather_readings[MEAN_HUMIDITY].append(int(info[MEAN_HUMIDITY_INDEX])
                                                       if info[MEAN_HUMIDITY_INDEX] != '' else None)

    return weather_readings


def parse_date(date):
    _, m, d = date.split('-')
    return MONTHS[int(m) - 1], d


def skip_none(x):
    return x is not None


def compute_year_info(weather_readings):
    dates = weather_readings[PKT]
    max_temps = weather_readings[MAX_TEMP]
    min_temps = weather_readings[MIN_TEMP]
    mean_humiditys = weather_readings[MEAN_HUMIDITY]

    highest_temp = max(filter(skip_none, max_temps))
    highest_temp_date = dates[list.index(max_temps, highest_temp)]
    highest_temp_month, highest_temp_day = parse_date(highest_temp_date)

    lowest_temp = min(filter(skip_none, min_temps))
    lowest_temp_date = dates[list.index(min_temps, lowest_temp)]
    lowest_temp_month, lowest_temp_day = parse_date(lowest_temp_date)

    most_humidity = max(filter(skip_none, mean_humiditys))
    most_humidity_date = dates[list.index(mean_humiditys, most_humidity)]
    most_humidity_month, most_humidity_day = parse_date(most_humidity_date)

    results = ((highest_temp, highest_temp_month, highest_temp_day),
               (lowest_temp, lowest_temp_month, lowest_temp_day),
               (most_humidity, most_humidity_month, most_humidity_day)
               )
    return results


def compute_month_info(weather_readings):
    max_temps = weather_readings[MAX_TEMP]
    min_temps = weather_readings[MIN_TEMP]
    mean_humiditys = weather_readings[MEAN_HUMIDITY]

    highest_average = statistics.mean(filter(skip_none, max_temps))
    lowest_average = statistics.mean(filter(skip_none, min_temps))
    average_mean_humidity = statistics.mean(filter(skip_none, mean_humiditys))

    return highest_average, lowest_average, average_mean_humidity


def compute_month_temp_detail(weather_readings):
    dates = weather_readings[PKT]
    max_temps = weather_readings[MAX_TEMP]
    min_temps = weather_readings[MIN_TEMP]

    days = [parse_date(date)[1] for date in dates]

    return days, max_temps, min_temps


def main():
    # creating argument parser
    # parser = argparse.ArgumentParser()
    # parser.add_argument('files_dir',
    #                     type=str,
    #                     help='Directory containing weather files')
    # parser.add_argument('-e',
    #                     metavar='e',
    #                     type=str,
    #                     nargs='?',
    #                     help=('For a given year display the highest temperature and day, lowest temperature and day, '
    #                           'most humid day and humidity.'))
    # parser.add_argument('-a',
    #                     metavar='a',
    #                     type=str,
    #                     nargs='?',
    #                     help=('For a given month display the average highest temperature, average lowest temperature, '
    #                           'average mean humidity.'))
    # parser.add_argument('-c',
    #                     metavar='c',
    #                     type=str,
    #                     nargs='?',
    #                     help=(
    #                         'For a given month draw two horizontal bar charts on the console for the highest and '
    #                         'lowest temperature on each day. Highest in red and lowest in blue.'))
    # args = parser.parse_args()

    # extracting arguments
    files_dir = 'weatherfiles/'  # args.files_dir + '/'
    e = None  # args.e
    a = None  # args.a
    c = '2011/3'  # args.c

    if e is not None:
        year = e
        files_prefix = 'Murree_weather_{year}_'.format(year=year)
        year_file_names = [file for file in os.listdir(files_dir)
                           if file.startswith(files_prefix)]
        weather_readings = parse(files_dir, year_file_names)
        results = compute_year_info(weather_readings)
        report_generator.generate_year_info_report(results)

    if a is not None:
        year, month = a.split('/')
        file_name = 'Murree_weather_{year}_{month}.txt'.format(year=year, month=MONTHS_ABBREVIATED[int(month) - 1])
        weather_readings = parse(files_dir, [file_name])
        results = compute_month_info(weather_readings)
        report_generator.generate_month_info_report(results)

    if c is not None:
        year, month = c.split('/')
        file_name = 'Murree_weather_{year}_{month}.txt'.format(year=year, month=MONTHS_ABBREVIATED[int(month) - 1])
        weather_readings = parse(files_dir, [file_name])
        results = compute_month_temp_detail(weather_readings)
        report_generator.generate_month_temp_detailed_report(results)


main()
