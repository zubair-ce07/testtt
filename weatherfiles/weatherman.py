import os
import sys
from os import listdir
import csv
import calendar
from termcolor import colored
import re


class WeatherFilesParser:
    
    def __init__(self):
        pass
    
    #Get all files from given dirctory path
    def get_all_files(self, path, key = None):
        files = []
        for file_name in listdir(path):
            if file_name.endswith(".txt"):
                file_path = path + "/" + file_name
                files.append(file_path)
        
        return files
    
    def read_file(self, file_path):
        file_data = []
        with open(file_path, 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)

            for row in csv_reader:
                file_data.append(row)
        return file_data
    
    #Populate weather data
    def read_weather_files(self, files):
        weather_data = []
        for file_path in files:
            file_data = self.read_file(file_path)
            weather_data.extend(file_data)
        return weather_data


class WeatherResultCalculation:
    
    def __init__(self):
        pass
    
    def filter_weather_data(self, weather_data, key):
        filtered_data = []
        for row in weather_data:
            if key in row[0]:
                filtered_data.append(row)
        return filtered_data
    
    def calculate_annual_weather_results(self, weather_data, year):
        filtered_weather_data = self.filter_weather_data(weather_data, year)
        if not filtered_weather_data:
            return -1
        
        #Hold annual calculated results
        annaul_results = {}
        
        #Find highest temprature and day
        max_tempr_list = [int(row[1]) for row in filtered_weather_data if row[1]]
        if max_tempr_list:
            max_tempr = max(max_tempr_list)
            max_tempr_date = filtered_weather_data[max_tempr_list.index(max_tempr)][0]
            annaul_results["max_tempr"] = [max_tempr, max_tempr_date]
        else: annaul_results["max_tempr"] = [None, None]
            
        #Find lowest temprature and day
        min_tempr_list = [int(row[3]) for row in filtered_weather_data if row[3]]
        if min_tempr_list:
            min_tempr = min(min_tempr_list)
            min_tempr_date = filtered_weather_data[min_tempr_list.index(min_tempr)][0]
            annaul_results["min_tempr"] = [min_tempr, min_tempr_date]
        else: annaul_results["min_tempr"] = [None, None]
            
        #Find highest humidity and day
        max_humidity_list = [int(row[7]) for row in filtered_weather_data if row[7]]
        if max_humidity_list:
            max_humidity = max(max_humidity_list)
            max_humidity_date = filtered_weather_data[max_humidity_list.index(max_humidity)][0]
            annaul_results["max_humidity"] = [max_humidity, max_humidity_date]
        else: annaul_results["max_humidity"] = [None, None]
        
        return annaul_results
    
    def calculate_monthly_weather_results(self, weather_data, year_month):
        year, month = map(int, year_month.split("/"))
        year_month = '{}-{}'.format(year, month)
        
        filtered_weather_data = self.filter_weather_data(weather_data, year_month)
        if not filtered_weather_data:
            return -1
        
        #Hold monthly calculated results
        monthly_results = {}
        
        #Find average_highest_temprature
        max_tempr_list = [int(row[1]) for row in filtered_weather_data if row[1]]
        if max_tempr_list:
            highest_avg_tempr = sum(max_tempr_list)//calendar.monthrange(year, month)[1]
            monthly_results["highest_avg_tempr"] = highest_avg_tempr
        else: monthly_results["max_tempr"] = None
            
        #Find average_lowest_temprature
        min_tempr_list = [int(row[3]) for row in filtered_weather_data if row[3]]
        if min_tempr_list:
            lowest_avg_tempr = sum(min_tempr_list)//calendar.monthrange(year, month)[1]
            monthly_results["lowest_avg_tempr"] = lowest_avg_tempr
        else: monthly_results["lowest_avg_tempr"] = None
        
        #Find average mean humidity
        mean_humidity_list = [int(row[8]) for row in filtered_weather_data if row[8]]
        if mean_humidity_list:
            avg_mean_humidity = sum(mean_humidity_list)//calendar.monthrange(year, month)[1]
            monthly_results["avg_mean_humidity"] = avg_mean_humidity
        else: monthly_results["avg_mean_humidity"] = None
            
        return monthly_results
    
    def get_month_temprature_readings(self, weather_data, year_month):
        year, month = map(int, year_month.split("/"))
        year_month = '{}-{}'.format(year, month)
        
        filtered_weather_data = self.filter_weather_data(weather_data, year_month)
        if not filtered_weather_data:
            return -1
        
        #Hold highes, lowest temprature reading for a month
        month_temprature_readings = {}
        
        month_temprature_readings['year_month'] = year_month
        month_temprature_readings['max_tempr'] = [int(row[1]) if row[1] else None for row in filtered_weather_data]
        month_temprature_readings['min_tempr'] = [int(row[3]) if row[3] else None for row in filtered_weather_data]
        
        return month_temprature_readings


class GenerateWeatherReports:
    
    def __init__(self):
        pass
    
    def get_month_name(self, date):
        ind = int(date.split("-")[1])
        return calendar.month_name[ind]
    
    def get_day(self, date):
        return int(date.split("-")[2])
    
    def generate_annual_report(self, annual_results):
        print('Highest: {}C on {} {}'.format(annual_results['max_tempr'][0], 
                                             self.get_month_name(annual_results['max_tempr'][1]),
                                             self.get_day(annual_results['max_tempr'][1])))
        print('Lowest: {}C on {} {}'.format(annual_results['min_tempr'][0], 
                                             self.get_month_name(annual_results['min_tempr'][1]),
                                             self.get_day(annual_results['min_tempr'][1])))
        print('Humidity: {}% on {} {}'.format(annual_results['max_humidity'][0], 
                                             self.get_month_name(annual_results['max_humidity'][1]),
                                             self.get_day(annual_results['max_humidity'][1])))
        
    def generate_monthly_report(self, monthly_results):
        print('Highest Average: {}C'.format(monthly_results['highest_avg_tempr']))
        print('Lowest Average: {}C'.format(monthly_results['lowest_avg_tempr']))
        print('Average Mean Humidity: {}%'.format(monthly_results['avg_mean_humidity']))
        
    def generate_month_temprature_report(self, month_temprature_readings):
        max_tempr_list = month_temprature_readings['max_tempr']
        max_tempr_list = month_temprature_readings['min_tempr']
        year, month = month_temprature_readings['year_month'].split("-")
        
        print('{} {}'.format(calendar.month_name[int(month)], year))
        i = 0
        for h_tempr, m_tempr in zip(max_tempr_list, max_tempr_list):
            h_tempr_str = ''
            m_tempr_str = ''
            day = '{num:02d}'.format(num=i + 1)
            if h_tempr:
                h_tempr_str = colored('+' * h_tempr, 'red')
            if m_tempr:
                m_tempr_str = colored('+' * m_tempr, 'blue')
                
            print('{}{}{} {}C - {}C'.format(day, m_tempr_str, h_tempr_str, m_tempr, h_tempr))
            
            i = i + 1


if __name__ == '__main__':
    path = sys.argv[1]
    parser = WeatherFilesParser()
    files_list = parser.get_all_files(path)
    weather_data = parser.read_weather_files(files_list)

    arguments = sys.argv[2:]

    for i in range(0, len(arguments), 2):
        report_type, date = arguments[i:i + 2]

        w_r_cal = WeatherResultCalculation()
        g_r = GenerateWeatherReports()

        if report_type == "-e":
            if re.match(r'[0-9]{4}', date):
                annual_results = w_r_cal.calculate_annual_weather_results(weather_data, date)
                if annual_results != -1:
                    g_r.generate_annual_report(annual_results)
                else:
                    print("No weather data available for given year")
            else:
                print("Error: Invalid argument 'year'")
                sys.exit()
        elif report_type == "-a":
            if len(date.split('/')) == 2:
                month_results = w_r_cal.calculate_monthly_weather_results(weather_data, date)
                if month_results != -1:
                    g_r.generate_monthly_report(month_results)
                else:
                    print("No weather data available for given month")
            else:
                print("Error: Invalid argument 'date', it should be year/month format")
                sys.exit()
        elif report_type == "-c":
            if len(date.split('/')) == 2:
                month_tempr_list = w_r_cal.get_month_temprature_readings(weather_data, date)
                if month_tempr_list != -1:
                    g_r.generate_month_temprature_report(month_tempr_list)
                else:
                    print("No weather data available for given month")
            else:
                print("Error: Invalid argument 'date', it should be year/month format")
                sys.exit()
    
