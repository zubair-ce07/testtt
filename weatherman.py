import os
import csv
import glob
import argparse

from enum import Enum
from datetime import datetime


class WeatherReport(Enum):
    annual_min_max_temperature = "1"
    annual_max_temperature = "2"
    annual_min_temperature = "3"


class WeatherData:
    def __init__(self, date, max_temperature, min_temperature,
                 max_humidity, min_humidity):
        self.date = date
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.max_humidity = max_humidity
        self.min_humidity = min_humidity


def import_data_from_files(data_dir):
    os.chdir(data_dir)

    weather_data_dict = {}

    for weather_file in glob.glob('*.txt'):
        with open(weather_file, "r") as csvfile:
            readable_lines = csvfile.readlines()[1:-1]
            reader = csv.DictReader(readable_lines)

            max_temp = -100
            min_temp = 100
            max_humid = -1
            min_humid = 101

            for row in reader:
                date = row.get('PKT') or row.get('PKST')
                year = datetime.strptime(str(date), "%Y-%m-%d").year
                if row['Max TemperatureC']:
                    max_temp = int(row.get('Max TemperatureC'))
                if row['Max TemperatureC']:
                    min_temp = int(row.get('Min TemperatureC'))
                if row['Max TemperatureC']:
                    max_humid = int(row.get('Max Humidity'))
                if row['Max TemperatureC']:
                    min_humid = int(row.get(' Min Humidity'))
                if year not in weather_data_dict:
                    weather_data_dict[year] = []
                weather_data_dict[year].append(
                    WeatherData(date, max_temp, min_temp, max_humid, min_humid))
    return weather_data_dict


def valid(data_dir=''):
    if not os.path.isdir(data_dir):
        print("Weather data directory does not exist")
        return False

    return True


def print_yearly_coldest_day(weather_data_dict):
    print("Coldest day of each year")
    print ('%s\t\t%s\t\t\t\t%s' % ("Year", "Date", "Temp"))
    print ('------------------------------------------------------------')
    for year, year_weather in weather_data_dict.items():
        year_weather.sort(key=lambda x: x.min_temperature, reverse=False)
        print ('%s\t\t%s\t\t\t%s' % (
            str(year),
            str(year_weather[0].date),
            year_weather[0].min_temperature))


def print_yearly_hottest_day(weather_data_dict):
    print("Hottest day of each year")
    print ('%s\t\t%s\t\t\t\t%s' % ("Year", "Date", "Temp"))
    print ('------------------------------------------------------------')
    for year, year_weather in weather_data_dict.items():
        year_weather.sort(key=lambda x: x.max_temperature, reverse=True)
        print ('%s\t\t%s\t\t\t%s' % (
            str(year),
            str(year_weather[0].date),
            year_weather[0].max_temperature))


def print_yearly_report(weather_data_dict):
    print("Annual Max/Min Temperature")
    print ('%s\t%s\t%s\t%s\t%s' % (
        "Year",
        "Max TemperatureC",
        "Min TemperatureC",
        "Max Humidity",
        "Min Humidity"))
    print (
        '------------------------------------------------------------------------------------------')
    for year, year_weather in weather_data_dict.items():
        year_weather.sort(key=lambda x: x.max_temperature, reverse=True)
        max_temp = str(year_weather[0].max_temperature)
        year_weather.sort(key=lambda x: x.min_temperature, reverse=False)
        min_temp = str(year_weather[0].min_temperature)
        year_weather.sort(key=lambda x: x.max_humidity, reverse=True)
        max_humid = str(year_weather[0].max_humidity)
        year_weather.sort(key=lambda x: x.min_humidity, reverse=False)
        min_humid = str(year_weather[0].min_humidity)

        print ('%s\t\t%s\t\t\t%s\t\t\t%s\t\t%s' % (
            str(year),
            max_temp,
            min_temp,
            max_humid,
            min_humid))


def print_weather_report(weather_data_dict, report_no):
    if report_no == WeatherReport.annual_min_max_temperature.value:
        print_yearly_report(weather_data_dict)
    elif report_no == WeatherReport.annual_max_temperature.value:
        print_yearly_hottest_day(weather_data_dict)
    elif report_no == WeatherReport.annual_min_temperature.value:
        print_yearly_coldest_day(weather_data_dict)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "report_no",
        help="1 for Annual Max/Min Temperature "
             + "\n2 for Hottest day of each year "
             + "\n3 for coldest day of each year",
        choices=["1", "2", "3"])
    parser.add_argument(
        "data_dir",
        help="Directory containing weather data files")
    args = parser.parse_args()

    if valid(args.data_dir):
        weather_data_dict = import_data_from_files(args.data_dir)
        print_weather_report(weather_data_dict, args.report_no)


if __name__ == "__main__":
    main()
