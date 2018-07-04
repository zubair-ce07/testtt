import os
import sys
import csv
import re
import argparse
from termcolor import colored
from time import strptime, strftime


class WeatherFilesParser:
    
    def __get_int(self, value):
        return int(value) if value else None

    # Populate weather data
    def __get_readings(self, row):
        reading = {}
        reading['PKT'] = row.get('PKT') if row.get('PKT') else row.get('PKST')
        reading['Max TemperatureC'] = self.__get_int(row.get('Max TemperatureC'))
        reading['Min TemperatureC'] = self.__get_int(row.get('Min TemperatureC'))
        reading['Max Humidity'] = self.__get_int(row.get('Max Humidity'))
        reading['Mean Humidity'] = self.__get_int(row.get(' Mean Humidity'))
    
        return reading

    def get_filtered_files(self, path, file_key):
        if os.path.isdir(path):
            files = list(filter(lambda f : f.endswith(".txt") and file_key in f, os.listdir(path)))
  
            if files: return map(lambda f : os.path.join(path, f), files)
            else: raise ValueError("Weather Readings Not Available for Given Query")

        else:
            raise OSError("Directory does not exist " + path)

    def read_weather_file(self, file_path):
        readings = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
               readings.append(self.__get_readings(r))

            return readings

    def read_all_files(self, path, file_key):
        weather_readings = []
        for file_path in self.get_filtered_files(path, file_key):
            file_data = self.read_weather_file(file_path)
            weather_readings.extend(file_data)

        return weather_readings


class WeatherResultCalculation:

    def max_field(self, weather_readings, field_name):
        filtered_readings = list(filter(lambda r : r[field_name], weather_readings))

        return max(filtered_readings, key=lambda r : r[field_name])

    def min_field(self, weather_readings, field_name):
        filtered_readings = list(filter(lambda r : r[field_name], weather_readings))

        return min(filtered_readings, key=lambda r : r[field_name])

    def average_field(self, weather_readings, field_name):
        filtered_readings = list(filter(lambda r : r[field_name], weather_readings))

        return sum(r[field_name] for r in filtered_readings)//len(filtered_readings)


     
class GenerateWeatherReports:

    def __init__(self):
        self.weather_cal = WeatherResultCalculation()

    def generate_annual_report(self, weather_readings):
        max_tempr_row = self.weather_cal.max_field(weather_readings, 'Max TemperatureC')
        min_tempr_row = self.weather_cal.min_field(weather_readings, 'Min TemperatureC')
        max_humidity_row = self.weather_cal.max_field(weather_readings, 'Max Humidity')

        max_tempr_date = strftime('%B %d', strptime(max_tempr_row['PKT'], '%Y-%m-%d'))
        min_tempr_date = strftime('%B %d', strptime(min_tempr_row['PKT'], '%Y-%m-%d'))
        max_humidity_date = strftime('%B %d', strptime(max_humidity_row['PKT'], '%Y-%m-%d'))
    
        print(f'Highest: {max_tempr_row["Max TemperatureC"]}C on {max_tempr_date}')
        print(f'Lowest: {min_tempr_row["Min TemperatureC"]}C on {min_tempr_date}')
        print(f'Humidity: {max_humidity_row["Max Humidity"]}C on {max_humidity_date}')
 
    def generate_monthly_report(self, weather_readings):
        max_tempr_avg = self.weather_cal.average_field(weather_readings, 'Max TemperatureC')
        min_tempr_avg = self.weather_cal.average_field(weather_readings, 'Min TemperatureC')
        mean_humidity_avg = self.weather_cal.average_field(weather_readings, 'Mean Humidity')

        print(f"Highest Average: {max_tempr_avg}C")
        print(f"Lowest Average: {min_tempr_avg}C")
        print(f"Average Mean Humidity: {mean_humidity_avg}%")
                
    def generate_month_temprature_report(self, weather_readings, month):
        filtered_readings = list(filter(lambda r : r['Max TemperatureC'], weather_readings))
        month = strftime('%B %Y', strptime(month, '%Y_%b'))
        print(f'{month}')
        for row in filtered_readings:
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

def check_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path",
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
        parser = WeatherFilesParser()
        weather_readings = parser.read_all_files(args.folder_path, args.e)

        weather_rep = GenerateWeatherReports()
        weather_rep.generate_annual_report(weather_readings)
    if args.a:
        parser = WeatherFilesParser()
        weather_readings = parser.read_all_files(args.folder_path, args.a)

        weather_rep = GenerateWeatherReports()
        weather_rep.generate_monthly_report(weather_readings)
    if args.c:
        parser = WeatherFilesParser()
        weather_readings = parser.read_all_files(args.folder_path, args.c)

        weather_rep = GenerateWeatherReports()
        weather_rep.generate_month_temprature_report(weather_readings, args.c)
