import os
import csv
import glob
import argparse

from enum import IntEnum
from datetime import datetime


class WeatherReport(IntEnum):
    annual_min_max_reading = 1
    annual_max_temperature = 2
    annual_min_temperature = 3


class WeatherReading:
    def __init__(self, date, max_temperature, min_temperature,
                 max_humidity, min_humidity):
        self.date = date
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.max_humidity = max_humidity
        self.min_humidity = min_humidity

    def __repr__(self):
        return "WeatherReading(%s,%s,%s,%s,%s)" % (self.date,
                                                   self.max_temperature,
                                                   self.min_temperature,
                                                   self.max_humidity,
                                                   self.min_humidity)


def import_data_from_files(data_dir):
    weather_readings = {}
    for weather_file in glob.glob(data_dir + '*.txt'):
        with open(weather_file, "r") as csvfile:
            readable_lines = csvfile.readlines()[1:-1]
            reader = csv.DictReader(readable_lines)

            for row in reader:
                date = row.get('PKT') or row.get('PKST')
                year = datetime.strptime(str(date), "%Y-%m-%d").year
                max_temp = int(row.get('Max TemperatureC') or -100)
                min_temp = int(row.get('Min TemperatureC') or 100)
                max_humid = int(row.get('Max Humidity') or -1)
                min_humid = int(row.get(' Min Humidity') or 101)
                if year not in weather_readings:
                    weather_readings[year] = []
                weather_readings[year].append(
                    WeatherReading(date, max_temp, min_temp, max_humid, min_humid))
    return weather_readings


def get_yearly_coldest_days(weather_readings):
    coldest_days = {}
    for year, year_weather in weather_readings.items():
        min_temp = min(year_weather, key=lambda x: x.min_temperature)
        coldest_days[year] = min_temp
    return coldest_days


def get_yearly_hottest_days(weather_readings):
    hottest_days = {}
    for year, year_weather in weather_readings.items():
        max_temp = max(year_weather, key=lambda x: x.max_temperature)
        hottest_days[year] = max_temp
    return hottest_days


def get_yearly_min_max_readings(weather_readings):
    yearly_min_max_readings = {}
    for year, year_weather_reading in weather_readings.items():
        max_temp = max(year_weather_reading, key=lambda x: x.max_temperature)
        min_temp = min(year_weather_reading, key=lambda x: x.min_temperature)
        max_humid = max(year_weather_reading, key=lambda x: x.max_humidity)
        min_humid = min(year_weather_reading, key=lambda x: x.min_humidity)

        yearly_min_max_readings[year] = WeatherReading(str(year) + "-1-1",
                                                       max_temp.max_temperature,
                                                       min_temp.min_temperature,
                                                       max_humid.max_humidity,
                                                       min_humid.min_humidity)
    return yearly_min_max_readings


def print_yearly_coldest_day(coldest_days):
    print("Coldest day of each year")
    print('%s\t\t%s\t\t\t\t%s' % ("Year", "Date", "Temp"))
    print('------------------------------------------------------------')
    for year, coldest_day in coldest_days.items():
        print('%s\t\t%s\t\t\t%s' % (
            year,
            coldest_day.date,
            coldest_day.min_temperature))


def print_yearly_hottest_day(hottest_days):
    print("Hottest day of each year")
    print('%s\t\t%s\t\t\t\t%s' % ("Year", "Date", "Temp"))
    print('------------------------------------------------------------')
    for year, hottest_day in hottest_days.items():
        print('%s\t\t%s\t\t\t%s' % (
            year,
            hottest_day.date,
            hottest_day.max_temperature))


def print_yearly_report(yearly_min_max_readings):
    print("Annual Max/Min Temperature")
    print('%s\t%s\t%s\t%s\t%s' % (
        "Year",
        "Max TemperatureC",
        "Min TemperatureC",
        "Max Humidity",
        "Min Humidity"))
    print(
        '------------------------------------------------------------------------------------------')
    for year, yearly_reading in yearly_min_max_readings.items():
        print('%d\t\t%s\t\t\t%s\t\t\t%s\t\t%s' % (
            year,
            yearly_reading.max_temperature,
            yearly_reading.min_temperature,
            yearly_reading.max_humidity,
            yearly_reading.min_humidity))


def print_weather_report(weather_readings, report_no):
    if report_no == WeatherReport.annual_min_max_reading.value:
        yearly_min_max_readings = get_yearly_min_max_readings(weather_readings)
        print_yearly_report(yearly_min_max_readings)
    elif report_no == WeatherReport.annual_max_temperature.value:
        hottest_days = get_yearly_hottest_days(weather_readings)
        print_yearly_hottest_day(hottest_days)
    elif report_no == WeatherReport.annual_min_temperature.value:
        coldest_days = get_yearly_coldest_days(weather_readings)
        print_yearly_coldest_day(coldest_days)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "report_no",
        help="1 for Annual Max/Min Temperature "
             + "\n2 for Hottest day of each year "
             + "\n3 for coldest day of each year",
        choices=[1, 2, 3],
        type=int)
    parser.add_argument(
        "data_dir",
        help="Directory containing weather data files")
    args = parser.parse_args()

    if os.path.isdir(args.data_dir):
        weather_readings = import_data_from_files(args.data_dir)
        print_weather_report(weather_readings, args.report_no)
    else:
        print("Weather data directory does not exist")


if __name__ == "__main__":
    main()
