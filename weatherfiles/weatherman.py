import os
import sys
import csv
import calendar
import re
import argparse
from termcolor import colored
from collections import defaultdict
from time import strptime


class WeatherFilesParser:
    
    #Get all files from given dirctory path
    def get_filtered_files(self, path, key):
        if os.path.isdir(path):
            return [path + "/" + file_name for file_name in os.listdir(path) if (file_name.endswith(".txt") and key in file_name)]
        else: 
            raise OSError("Directory does not exist " + path)
    
    def read_weather_file(self, file_path):
        fieldnames = ('PKT', 'Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC', 'Dew PointC', 'MeanDew PointC',
                      'Min DewpointC', 'Max Humidity', 'Mean Humidity', 'Min Humidity', 'Max Sea Level PressurehPa', 
                      'Mean Sea Level PressurehPa', 'Min Sea Level PressurehPa', 'Max VisibilityKm', 'Mean VisibilityKm', 
                      'Min VisibilitykM', 'Max Wind SpeedKm/h', 'Mean Wind SpeedKm/h', 'Max Gust SpeedKm/h', 'Precipitationmm', 
                      'CloudCover', 'Events', 'WindDirDegrees')
        try:
            with open(file_path, 'r') as f:
                csv_reader = csv.DictReader(f, fieldnames = fieldnames)
                next(csv_reader)                       #skip header row
                return [row for row in csv_reader]
        except IOError:
            print ("Could not read file:" + file_path)
    
    #Populate weather data
    def read_all_files(self, files):
        weather_readings = []
        for file_path in files:
            file_data = self.read_weather_file(file_path)
            weather_readings.extend(file_data)
        return weather_readings


class WeatherResultCalculation:
    
    def filter_weather_readings(self, weather_readings, key):
        return [row for row in weather_readings if key in row['PKT']]
    
    def calculate_annual_weather_results(self, filtered_weather_readings):        
        #Hold annual calculated results
        annaul_results = defaultdict(lambda: None)
        
        #Find highest temprature and day
        max_tempr_list = [int(row['Max TemperatureC']) for row in filtered_weather_readings if row['Max TemperatureC']]
        if max_tempr_list:
            annaul_results["max_tempr"] = max(max_tempr_list)
            annaul_results["max_tempr_date"] = filtered_weather_readings[max_tempr_list.index(annaul_results["max_tempr"])]['PKT']
            
        #Find lowest temprature and day
        min_tempr_list = [int(row['Min TemperatureC']) for row in filtered_weather_readings if row['Min TemperatureC']]
        if min_tempr_list:
            annaul_results["min_tempr"] = min(min_tempr_list)
            annaul_results["min_tempr_date"] = filtered_weather_readings[min_tempr_list.index(annaul_results["min_tempr"])]['PKT']
            
        #Find highest humidity and day
        max_humidity_list = [int(row['Max Humidity']) for row in filtered_weather_readings if row['Max Humidity']]
        if max_humidity_list:
            annaul_results["max_humidity"] = max(max_humidity_list)
            annaul_results["max_humidity_date"] = filtered_weather_readings[max_humidity_list.index(annaul_results["max_humidity"])]['PKT']
        
        return annaul_results
    
    def calculate_monthly_weather_results(self, filtered_weather_readings, year_month):
        year, month = year_month.split("_")
        year = int(year)
        month = strptime(month,'%b').tm_mon
        
        #Hold monthly calculated results
        monthly_results = defaultdict(lambda: None)
        
        #Find average_highest_temprature
        max_tempr_list = [int(row['Max TemperatureC']) for row in filtered_weather_readings if row['Max TemperatureC']]
        if max_tempr_list:
            monthly_results["highest_avg_tempr"] = sum(max_tempr_list)//calendar.monthrange(year, month)[1]
            
        #Find average_lowest_temprature
        min_tempr_list = [int(row['Min TemperatureC']) for row in filtered_weather_readings if row['Min TemperatureC']]
        if min_tempr_list:
            monthly_results["lowest_avg_tempr"] = sum(min_tempr_list)//calendar.monthrange(year, month)[1]
        
        #Find average mean humidity
        mean_humidity_list = [int(row['Mean Humidity']) for row in filtered_weather_readings if row['Mean Humidity']]
        if mean_humidity_list:
            monthly_results["avg_mean_humidity"] = sum(mean_humidity_list)//calendar.monthrange(year, month)[1]
            
        return monthly_results
    
    def get_month_temprature_readings(self, weather_readings, year_month):      
        #Hold highes, lowest temprature reading for a month
        month_temprature_readings = defaultdict(lambda: None)
        
        month_temprature_readings['year_month'] = year_month
        month_temprature_readings['max_tempr'] = [int(row['Max TemperatureC']) if row['Max TemperatureC'] else None for row in weather_readings]
        month_temprature_readings['min_tempr'] = [int(row['Min TemperatureC']) if row['Min TemperatureC'] else None for row in weather_readings]
        
        return month_temprature_readings


class GenerateWeatherReports:
    
    def get_month_name(self, date):
        ind = int(date.split("-")[1])
        return calendar.month_name[ind]
    
    def get_day(self, date):
        return int(date.split("-")[2])
    
    def generate_annual_report(self, annual_results):
        print('Highest: {}C on {} {}'.format(annual_results['max_tempr'], 
                                             self.get_month_name(annual_results['max_tempr_date']),
                                             self.get_day(annual_results['max_tempr_date'])))
        print('Lowest: {}C on {} {}'.format(annual_results['min_tempr'], 
                                             self.get_month_name(annual_results['min_tempr_date']),
                                             self.get_day(annual_results['min_tempr_date'])))
        print('Humidity: {}% on {} {}'.format(annual_results['max_humidity'], 
                                             self.get_month_name(annual_results['max_humidity_date']),
                                             self.get_day(annual_results['max_humidity_date'])))
        
    def generate_monthly_report(self, monthly_results):
        print(f"Highest Average: {monthly_results['highest_avg_tempr']}C")
        print(f"Lowest Average: {monthly_results['lowest_avg_tempr']}C")
        print(f"Average Mean Humidity: {monthly_results['avg_mean_humidity']}%")
        
    def generate_month_temprature_report(self, month_temprature_readings):
        max_tempr_list = month_temprature_readings['max_tempr']
        max_tempr_list = month_temprature_readings['min_tempr']
        year, month = month_temprature_readings['year_month'].split("_")
        
        print('{} {}'.format(calendar.month_name[strptime(month,'%b').tm_mon], year))
        i = 0
        for highest_tempr, min_tempr in zip(max_tempr_list, max_tempr_list):
            highest_tempr_bar = ''
            mim_tempr_bar = ''
            day = '{num:02d}'.format(num=i + 1)
            if highest_tempr:
                highest_tempr_bar = colored('+' * highest_tempr, 'red')
            if min_tempr:
                mim_tempr_bar = colored('+' * min_tempr, 'blue')
                
            print('{}{}{} {}C - {}C'.format(day, mim_tempr_bar, highest_tempr_bar, min_tempr, highest_tempr))
            
            i = i + 1


class CheckDateFormat(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values.split("/")) == 1:
            if not re.match(r'[0-9]{4}', values):
                raise ValueError("Insert Valid Year in format XXXX, i.e. 2004")                
        elif len(values.split("/")) == 2:
            if re.match(r'^(\d{4})/(0?[1-9]|1[012])$', values):
                values = values.split("/")[0] +"_"+ self.get_month_name(values.split("/")[1])
            else:
                raise ValueError("Insert Valid Month in format XXXX/XX, i.e. 2004/10")
        else:
            raise ValueError("Argument Not Valid")
        setattr(namespace, self.dest, values)
    
    def get_month_name(self, month):
        ind = int(month)
        return calendar.month_abbr[ind]


def check_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_folder",
                        help="Path of the folder that contains weather files")
    parser.add_argument("-e", "--year_report", type=str, action = CheckDateFormat,
                        help="Year to generate yearl report")
    parser.add_argument("-a", "--month_report", type=str, action = CheckDateFormat,
                        help="Specify the month to generate month report")
    parser.add_argument("-c", "--month_temprature", type=str, action = CheckDateFormat,
                        help="Specify the month to generate the charts for highest and lowest temprature")
    
    return parser.parse_args()


def get_weather_readings(path_to_folder, key):
    #Parse weather files from give path of folder
        parser = WeatherFilesParser()
        filtered_files = parser.get_filtered_files(path_to_folder, key)
        weather_readings = parser.read_all_files(filtered_files)

        if weather_readings: return weather_readings
        else: raise ValueError("Weather Readings Not Available for Given Query")

if __name__ == '__main__':
    args = check_args(sys.argv[1:])

    if args.year_report:
        weather_readings = get_weather_readings(args.path_to_folder, args.year_report)
        #Calculate weather results and generate reports
        w_r_cal = WeatherResultCalculation()
        g_r = GenerateWeatherReports()

        annual_results = w_r_cal.calculate_annual_weather_results(weather_readings)
        g_r.generate_annual_report(annual_results)
    if args.month_report:
        weather_readings = get_weather_readings(args.path_to_folder, args.month_report)
        #Calculate weather results and generate reports
        w_r_cal = WeatherResultCalculation()
        g_r = GenerateWeatherReports()

        month_results = w_r_cal.calculate_monthly_weather_results(weather_readings, args.month_report)
        g_r.generate_monthly_report(month_results)
    if args.month_temprature:
        weather_readings = get_weather_readings(args.path_to_folder, args.month_temprature)
        #Get weather results and generate reports
        w_r_cal = WeatherResultCalculation()
        g_r = GenerateWeatherReports()

        month_tempr_list = w_r_cal.get_month_temprature_readings(weather_readings, args.month_temprature)
        g_r.generate_month_temprature_report(month_tempr_list)
        