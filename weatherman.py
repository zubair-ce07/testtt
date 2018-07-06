import argparse
import datetime
import os
import csv

from weatherman_ds import WeatherReading
from weatherman_calculation import WeatherReport


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('directory')
    parser.add_argument('-e', default='')
    parser.add_argument('-a', default='')
    parser.add_argument('-c', default='')

    args = parser.parse_args()

    if args.e:
        weather_readings = load_data(args.directory, args.e)
        results = WeatherReport.yearly_results(weather_readings)
        extreme_weather_report(results)
    if args.a:
        month = args.a
        weather_readings = load_data(args.directory, month.split('/')[0], month.split('/')[1])
        results = WeatherReport.monthly_results(weather_readings)
        average_weather_report(results)


def load_data(directory='', year='', month=''):
        """Loads a given months data in the data structure"""
        files = []
        daily_readings = []
        if not month:
            for i in range(1, 13):
                month_abr = datetime.date(2000, i, 1).strftime('%b')
                file_path = directory + '/Murree_weather_' + year + "_" + month_abr + '.txt'
                if os.path.exists(file_path):
                    file = open(file_path, 'r')
                    files.append(file)
        else:
            month_abr = datetime.date(2000, int(month), 1).strftime('%b')
            file_path = directory + '/Murree_weather_' + year + "_" + month_abr + '.txt'
            if os.path.exists(file_path):
                file = open(file_path, 'r')
                files.append(file)

        for file in files:
            weather_csv = csv.DictReader(file)
            for row in weather_csv:
                daily_readings.append(WeatherReading(row))

        return daily_readings


def extreme_weather_report(result):
    """"Displays the highest lowest temperature and highest humidity report"""

    print("REPORT OPTION -e:")
    print("-"*18)

    high_day = datetime.datetime.strptime(result.highest_day, "%Y-%m-%d").strftime('%d %B')
    print("Highest: " + str(result.highest_reading) + "C on " + high_day)
    low_day = datetime.datetime.strptime(result.lowest_day, "%Y-%m-%d").strftime('%d %B')
    print("Lowest: " + str(result.lowest_reading) + "C on " + low_day)
    humid_day = datetime.datetime.strptime(result.humidity_day, "%Y-%m-%d").strftime('%d %B')
    print("Humidity: " + str(result.humidity_reading) + "% on " + humid_day)


def average_weather_report(result):
    """Displays the average highest lowest temperature and humidity of a month"""

    print("REPORT OPTION -a:")
    print("-"*18)

    print("Highest Average: " + str(result.highest_reading) + "C")
    print("Lowest Average: " + str(result.lowest_reading) + "C")
    print("Average mean humidity: " + str(result.humidity_reading) + "%")
    print("")


def option_c_report(data, date):
    """"Displays the bar chart for temperatures through the month"""
    months = ('January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December')

    print("REPORT OPTION -c:")
    print("-"*18)

    print(months[int(date[1])-1] + " " + date[0])
    month_data = data.pop()
    day_number = 1
    for day in month_data.days:
            min_temperature = day.readings["Min TemperatureC"]
            if min_temperature:
                reading_value = int(min_temperature)
                if reading_value >= 0:
                    print("\033[35m%02d" % day_number + "\033[34m" +
                          "+" * reading_value + "\033[30m", end="")
                else:
                    reading_value = abs(reading_value)
                    print("\033[35m%02d" % day_number + "\033[34m" +
                          "-" * reading_value + "\033[30m", end="")

            max_temperature = day.readings["Max TemperatureC"]
            if max_temperature:
                reading_value = int(max_temperature)
                if reading_value >= 0:
                    print("\033[31m" + "+"*reading_value + "\033[35m" +
                          min_temperature + "C-" +
                          max_temperature + "C\033[30m")
                else:
                    reading_value = abs(reading_value)
                    print("\033[31m" +
                          "-" * reading_value + "\033[35m" +
                          min_temperature + "C-" +
                          max_temperature + "C\033[30m")

            day_number += 1

    print("")


if __name__ == '__main__':
    main()
