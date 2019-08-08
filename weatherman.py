import argparse
import os
import statistics
import calendar
import csv

import dayinfo
import reportgenerator

PKT, PKT_INDEX = 'PKT', 0
MAX_TEMP, MAX_TEMP_INDEX = 'Max Temp', 1
MIN_TEMP, MIN_TEMP_INDEX = 'Min Temp', 3
MEAN_HUMIDITY, MEAN_HUMIDITY_INDEX = 'Mean Humidity', 8


def parse(files_dir, files):
    weather_readings = []

    for file in files:
        with open(files_dir + file) as f:
            reader = csv.DictReader(f)

            for info in reader:
                pkt = info['PKT']
                max_temp = int(info['Max TemperatureC']) if info['Max TemperatureC'] != '' else None
                min_temp = int(info['Min TemperatureC']) if info['Min TemperatureC'] != '' else None
                mean_humidity = int(info[' Mean Humidity']) if info[' Mean Humidity'] != '' else None
                weather_readings.append(dayinfo.DayInfo(pkt, max_temp, min_temp, mean_humidity))

    return weather_readings


def parse_date(date):
    _, m, d = date.split('-')
    return calendar.month_name[int(m)], d


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
    highest_average = statistics.mean(filter(skip_none,
                                             (weather_reading.max_temp for weather_reading in weather_readings)
                                             ))
    lowest_average = statistics.mean(filter(skip_none,
                                            (weather_reading.min_temp for weather_reading in weather_readings)
                                            ))
    average_mean_humidity = statistics.mean(filter(skip_none,
                                            (weather_reading.mean_humidity for weather_reading in weather_readings)
                                            ))

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
    a = '2011/03'  # args.a
    c = None  # args.c

    if e is not None:
        print(f'-e {e}')

        year = e
        files_prefix = f'Murree_weather_{year}_'
        year_file_names = [file for file in os.listdir(files_dir)
                           if file.startswith(files_prefix)]
        weather_readings = parse(files_dir, year_file_names)
        results = compute_year_info(weather_readings)
        reportgenerator.generate_year_info_report(results)

    if a is not None:
        print(f'-a {a}')

        year, month = a.split('/')
        month = calendar.month_abbr[int(month)]
        file_name = f'Murree_weather_{year}_{month}.txt'
        weather_readings = parse(files_dir, [file_name])
        results = compute_month_info(weather_readings)
        reportgenerator.generate_month_info_report(results)

    if c is not None:
        print(f'-c {c}')

        year, month = c.split('/')
        month = calendar.month_abbr[int(month)]
        file_name = f'Murree_weather_{year}_{month}.txt'
        weather_readings = parse(files_dir, [file_name])
        results = compute_month_temp_detail(weather_readings)
        reportgenerator.generate_month_temp_detailed_report(month=calendar.month_name[int(month)],
                                                            year=year,
                                                            results=results)


main()
