import os
import sys
import csv
import re
import argparse
from termcolor import colored
from time import strptime, strftime


class WeatherFilesParser:

    def __init__(self, path, file_pattern):
        self.path = path
        self.file_pattern = file_pattern
    
    def __get_readings(self, row):
        reading = {}
        if (
            row.get('Max TemperatureC') and row.get('Min TemperatureC') and
            row.get('Max Humidity') and row.get(' Mean Humidity')
            ):

            reading['PKT'] = row.get('PKT') or row.get('PKST')
            reading['Max TemperatureC'] = int(row.get('Max TemperatureC'))
            reading['Min TemperatureC'] = int(row.get('Min TemperatureC'))
            reading['Max Humidity'] = int(row.get('Max Humidity'))
            reading['Mean Humidity'] = int(row.get(' Mean Humidity'))
    
            return reading

    def get_filtered_files(self):
        files = list(filter(lambda f : f.endswith(".txt") and self.file_pattern in f, os.listdir(self.path)))
        return map(lambda f : os.path.join(self.path, f), files)

    def read_weather_file(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            return list(self.__get_readings(r) for r in reader if self.__get_readings(r))

    def read_all_files(self):
        weather_readings = []
        for file_path in self.get_filtered_files():
            file_readings = self.read_weather_file(file_path)
            weather_readings.extend(file_readings)

        return weather_readings


class WeatherResultCalculation:

    def max_field(self, weather_readings, field_name):
        return max(weather_readings, key=lambda r : r[field_name])

    def min_field(self, weather_readings, field_name):
        return min(weather_readings, key=lambda r : r[field_name])

    def average_field(self, weather_readings, field_name):
        return sum(r[field_name] for r in weather_readings)//len(weather_readings)


     
class GenerateWeatherReports(WeatherFilesParser):

    def __init__(self, folder_path, file_pattern):
        super().__init__(folder_path, file_pattern)
        self.weather_cal = WeatherResultCalculation()
    
    def __get_date(self, reading):
        return strftime('%B %d', strptime(reading['PKT'], '%Y-%m-%d'))

    def generate_annual_report(self):
        weather_readings = self.read_all_files()
        if not weather_readings:
            print(f'Weather readings not available for given query')
            return
        max_tempr_row = self.weather_cal.max_field(weather_readings, 'Max TemperatureC')
        min_tempr_row = self.weather_cal.min_field(weather_readings, 'Min TemperatureC')
        max_humidity_row = self.weather_cal.max_field(weather_readings, 'Max Humidity')

        max_tempr_date = self.__get_date(max_tempr_row)
        min_tempr_date = self.__get_date(min_tempr_row)
        max_humidity_date = self.__get_date(max_tempr_row)
    
        print(f'Highest: {max_tempr_row["Max TemperatureC"]}C on {max_tempr_date}')
        print(f'Lowest: {min_tempr_row["Min TemperatureC"]}C on {min_tempr_date}')
        print(f'Humidity: {max_humidity_row["Max Humidity"]}C on {max_humidity_date}')
 
    def generate_monthly_report(self):
        weather_readings = self.read_all_files()
        if not weather_readings:
            print(f'Weather readings not available for given query')
            return

        max_tempr_avg = self.weather_cal.average_field(weather_readings, 'Max TemperatureC')
        min_tempr_avg = self.weather_cal.average_field(weather_readings, 'Min TemperatureC')
        mean_humidity_avg = self.weather_cal.average_field(weather_readings, 'Mean Humidity')

        print(f"Highest Average: {max_tempr_avg}C")
        print(f"Lowest Average: {min_tempr_avg}C")
        print(f"Average Mean Humidity: {mean_humidity_avg}%")
                
    def generate_month_temprature_report(self, month):
        weather_readings = self.read_all_files()
        if not weather_readings:
            print(f'Weather readings not available for given query')
            return
        month = strftime('%B %Y', strptime(month, '%Y_%b'))
        print(f'{month}')
        for row in weather_readings:
            min_tempr = row['Min TemperatureC']
            max_tempr = row['Max TemperatureC']
            print(f'{strftime("%d", strptime(row["PKT"], "%Y-%m-%d"))}', end='')
            print(f'{colored("+"*min_tempr, "blue")}{colored("+"*max_tempr, "red")}{min_tempr}-{max_tempr}')
            


def check_date(value):
    if len(value.split("/")) == 1:
        if not re.match(r'[0-9]{4}', value):
            raise argparse.ArgumentTypeError(f'Invalid Year {value}')   

    elif len(value.split("/")) == 2:
        if re.match(r'^(\d{4})/(0?[1-9]|1[012])$', value):
            value = strftime('%Y_%b', strptime(value, '%Y/%m'))
        else:
            raise argparse.ArgumentTypeError(f'Invalid Month {value}')

    else:
        raise argparse.ArgumentTypeError(f'Argument Not Valid {value}') 

    return value

def is_path_exist(path):
    if os.path.isdir(path):
        return path
    raise OSError("Directory does not exist " + path)

def check_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path", type=is_path_exist,
                        help="Path of the folder that contains weather files")
    parser.add_argument("-e", type=check_date,
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
