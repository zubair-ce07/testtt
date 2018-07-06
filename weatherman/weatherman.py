import os
import sys
import csv
import re
import argparse
from termcolor import colored
from time import strptime, strftime

class Reading:
    def __init__(self, pkt, max_tempr, min_tempr, mean_humid, max_humid):
        self.pkt = pkt
        self.max_tempr = max_tempr
        self.min_tempr = min_tempr
        self.mean_humid = mean_humid
        self.max_humid = max_humid

class WeatherFilesParser:

    def __init__(self, path, file_pattern):
        self.path = path
        self.file_pattern = file_pattern
    
    def __get_fields(self, row):
        required_fields = ['Max TemperatureC', 'Min TemperatureC', 'Max Humidity', ' Mean Humidity']

        if all(row.get(f) for f in required_fields):

            return Reading(   row.get('PKT') or row.get('PKST'),
                              int(row.get('Max TemperatureC')),
                              int(row.get('Min TemperatureC')),
                              int(row.get('Max Humidity')),
                              int(row.get(' Mean Humidity'))
                            )

    def get_filtered_files(self):
        files = list(filter(lambda f : f.endswith(".txt") and self.file_pattern in f, os.listdir(self.path)))
        return map(lambda f : os.path.join(self.path, f), files)

    def read_weather_file(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            return list(filter(None, map(self.__get_fields, reader)))

    def read_all_files(self):
        weather_readings = []
        for file_path in self.get_filtered_files():
            file_readings = self.read_weather_file(file_path)
            weather_readings.extend(file_readings)

        return weather_readings


class WeatherResultCalculation:

    def __get_field(self, row, field_name):
        return row.__dict__.get(field_name)

    def max_field(self, weather_readings, field_name):
        return max(weather_readings, key=lambda r : self.__get_field(r, field_name))

    def min_field(self, weather_readings, field_name):
        return min(weather_readings, key=lambda r : self.__get_field(r, field_name))

    def average_field(self, weather_readings, field_name):
        return sum(self.__get_field(r, field_name) for r in weather_readings)//len(weather_readings)


     
class GenerateWeatherReports:

    def __init__(self, folder_path, date):
        if not isinstance(date, str):
            date = strftime('%Y_%b', date)

        self.file_parser = WeatherFilesParser(folder_path, date)
        self.weather_cal = WeatherResultCalculation()

    def __get_field(self, row, field_name):
        return row.__dict__.get(field_name)
    
    def __get_date(self, reading):
        return strftime('%B %d', strptime(self.__get_field(reading, 'pkt'), '%Y-%m-%d'))

    def generate_annual_report(self):
        weather_readings = self.file_parser.read_all_files()
        if weather_readings:
            max_tempr = self.weather_cal.max_field(weather_readings, 'max_tempr')
            min_tempr = self.weather_cal.min_field(weather_readings, 'min_tempr')
            max_humid = self.weather_cal.max_field(weather_readings, 'max_humid')

            max_tempr_date = self.__get_date(max_tempr)
            min_tempr_date = self.__get_date(min_tempr)
            max_humidity_date = self.__get_date(max_humid)
        
            print(f'Highest: {self.__get_field(max_tempr, "max_tempr")}C on {max_tempr_date}')
            print(f'Lowest: {self.__get_field(min_tempr, "min_tempr")}C on {min_tempr_date}')
            print(f'Humidity: {self.__get_field(max_humid, "max_humid")}C on {max_humidity_date}')

        else: print(f'Weather readings not available for given query')
 
    def generate_monthly_report(self):
        weather_readings = self.file_parser.read_all_files()
        if  weather_readings:
            max_tempr_avg = self.weather_cal.average_field(weather_readings, 'max_tempr')
            min_tempr_avg = self.weather_cal.average_field(weather_readings, 'min_tempr')
            mean_humidity_avg = self.weather_cal.average_field(weather_readings, 'mean_humid')

            print(f"Highest Average: {max_tempr_avg}C")
            print(f"Lowest Average: {min_tempr_avg}C")
            print(f"Average Mean Humidity: {mean_humidity_avg}%")

        else: print(f'Weather readings not available for given query')
                
    def generate_month_temprature_report(self, month):
        weather_readings = self.file_parser.read_all_files()
        if weather_readings:
            month = strftime('%B %Y', month)
            print(f'{month}')
            for r in weather_readings:
                min_tempr = self.__get_field(r, 'min_tempr')
                max_tempr = self.__get_field(r, 'max_tempr')
                print(f'{strftime("%d", strptime(self.__get_field(r, "pkt"), "%Y-%m-%d"))}', end='')
                print(f'{colored("+"*min_tempr, "blue")}{colored("+"*max_tempr, "red")}{min_tempr}-{max_tempr}')

        else: print(f'Weather readings not available for given query')
            


def check_date(value):
    if '/' not in value:
        raise argparse.ArgumentTypeError(f'Argument Not Valid {value}') 

    return strptime(value, '%Y/%m')

def check_year(value):
    if not re.match(r'[0-9]{4}', value):
        raise argparse.ArgumentTypeError(f'Invalid Year {value}')
    
    return value

def is_path_exist(path):
    if os.path.isdir(path):
        return path
    raise OSError("Directory does not exist " + path)

def check_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path", type=is_path_exist,
                        help="Path of the folder that contains weather files")
    parser.add_argument("-e", type=check_year,
                        help="Year to generate yearl report")
    parser.add_argument("-a", type=check_date,
                        help="Specify the month to generate month report")
    parser.add_argument("-c", type=check_date,
                        help="Specify the month to generate the charts for highest and lowest temprature")

    return parser.parse_args()


if __name__ == '__main__':
    args = check_args(sys.argv[1:])

    if args.e:
        weather_rep = GenerateWeatherReports(args.folder_path, args.e)
        weather_rep.generate_annual_report()
    if args.a:
        weather_rep = GenerateWeatherReports(args.folder_path, args.a)
        weather_rep.generate_monthly_report()
    if args.c:
        weather_rep = GenerateWeatherReports(args.folder_path, args.c)
        weather_rep.generate_month_temprature_report(args.c)
