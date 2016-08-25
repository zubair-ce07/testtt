import os
import csv
import glob
import argparse

from enum import IntEnum
from datetime import datetime


class WeatherReport(IntEnum):
    annual_min_max_temperature = 1
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


def import_data_from_files(data_dir):
    os.chdir(data_dir)

    weather_data = {}

    for weather_file in glob.glob('*.txt'):
        with open(weather_file, "r") as csvfile:
            readable_lines = csvfile.readlines()[1:-1]
            reader = csv.DictReader(readable_lines)

            for row in reader:
                date = row.get('PKT') or row.get('PKST')
                year = datetime.strptime(str(date), "%Y-%m-%d").year
                max_temp = int(row.get('Max TemperatureC') if row['Max TemperatureC'] else -100)
                min_temp = int(row.get('Min TemperatureC') if row['Max TemperatureC'] else 100)
                max_humid = int(row.get('Max Humidity') if row['Max TemperatureC'] else -1)
                min_humid = int(row.get(' Min Humidity') if row['Max TemperatureC'] else 101)
                if year not in weather_data:
                    weather_data[year] = []
                weather_data[year].append(
                    WeatherReading(date, max_temp, min_temp, max_humid, min_humid))
    return weather_data


def print_yearly_coldest_day(weather_data):
    print("Coldest day of each year")
    print('%s\t\t%s\t\t\t\t%s' % ("Year", "Date", "Temp"))
    print('------------------------------------------------------------')
    for year, year_weather in weather_data.items():
        min_temp = min(year_weather, key=lambda x: x.min_temperature)
        print('%s\t\t%s\t\t\t%s' % (
            str(year),
            str(min_temp.date),
            min_temp.min_temperature))


def print_yearly_hottest_day(weather_data):
    print("Hottest day of each year")
    print('%s\t\t%s\t\t\t\t%s' % ("Year", "Date", "Temp"))
    print('------------------------------------------------------------')
    for year, year_weather in weather_data.items():
        max_temp = max(year_weather, key=lambda x: x.max_temperature)
        print('%s\t\t%s\t\t\t%s' % (
            str(year),
            str(max_temp.date),
            max_temp.max_temperature))


def print_yearly_report(weather_data):
    print("Annual Max/Min Temperature")
    print('%s\t%s\t%s\t%s\t%s' % (
        "Year",
        "Max TemperatureC",
        "Min TemperatureC",
        "Max Humidity",
        "Min Humidity"))
    print(
        '------------------------------------------------------------------------------------------')
    for year, year_weather in weather_data.items():
        max_temp = max(year_weather, key=lambda x: x.max_temperature)
        min_temp = min(year_weather, key=lambda x: x.min_temperature)
        max_humid = max(year_weather, key=lambda x: x.max_humidity)
        min_humid = min(year_weather, key=lambda x: x.min_humidity)

        print('%s\t\t%s\t\t\t%s\t\t\t%s\t\t%s' % (
            str(year),
            max_temp.max_temperature,
            min_temp.min_temperature,
            max_humid.max_humidity,
            min_humid.min_humidity))


def print_weather_report(weather_data, report_no):
    if report_no == WeatherReport.annual_min_max_temperature.value:
        print_yearly_report(weather_data)
    elif report_no == WeatherReport.annual_max_temperature.value:
        print_yearly_hottest_day(weather_data)
    elif report_no == WeatherReport.annual_min_temperature.value:
        print_yearly_coldest_day(weather_data)


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
        weather_data = import_data_from_files(args.data_dir)
        print_weather_report(weather_data, args.report_no)
    else:
        print("Weather data directory does not exist")


if __name__ == "__main__":
    main()
