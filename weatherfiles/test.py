import os
import csv
import calendar
from collections import defaultdict
from termcolor import colored

class WeatherFilesParser:
    
    #Get all files from given dirctory path
    def get_all_files(self, path):
        if os.path.isdir(path):
            return [path + "/" + file_name for file_name in os.listdir(path) if file_name.endswith(".txt")]
        else: return -1
    
    def read_file(self, file_path):
        file_data = []
        with open(file_path, 'r') as f:
            csv_reader = csv.DictReader(f)
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
    
    def filter_weather_data(self, weather_data, key):
        print(weather_data[0]['PKT'])
        return [row for row in weather_data if key in row['PKT']]
    
    def calculate_annual_weather_results(self, weather_data, year):
        filtered_weather_data = self.filter_weather_data(weather_data, year)
        
        #Hold annual calculated results
        annaul_results = defaultdict(lambda: None)
        
        #Find highest temprature and day
        max_tempr_list = [int(row['Max TemperatureC']) for row in filtered_weather_data if row['Max TemperatureC']]
        if max_tempr_list:
            annaul_results["max_tempr"] = max(max_tempr_list)
            annaul_results["max_tempr_date"] = filtered_weather_data[max_tempr_list.index(annaul_results["max_tempr"])]['PKT']
            
        #Find lowest temprature and day
        min_tempr_list = [int(row['Min TemperatureC']) for row in filtered_weather_data if row['Min TemperatureC']]
        if min_tempr_list:
            annaul_results["min_tempr"] = min(min_tempr_list)
            annaul_results["min_tempr_date"] = filtered_weather_data[min_tempr_list.index(annaul_results["min_tempr"])]['PKT']
            
        #Find highest humidity and day
        max_humidity_list = [int(row['Max Humidity']) for row in filtered_weather_data if row['Max Humidity']]
        if max_humidity_list:
            annaul_results["max_humidity"] = max(max_humidity_list)
            annaul_results["max_humidity_date"] = filtered_weather_data[max_humidity_list.index(annaul_results["max_humidity"])]['PKT']
        
        return annaul_results
    
    def calculate_monthly_weather_results(self, weather_data, year_month):
        year, month = map(int, year_month.split("/"))
        year_month = '{}-{}'.format(year, month)
        
        filtered_weather_data = self.filter_weather_data(weather_data, year_month)
        
        #Hold monthly calculated results
        monthly_results = defaultdict(lambda: None)
        
        #Find average_highest_temprature
        max_tempr_list = [int(row['Max TemperatureC']) for row in filtered_weather_data if row['Max TemperatureC']]
        if max_tempr_list:
            monthly_results["highest_avg_tempr"] = sum(max_tempr_list)//calendar.monthrange(year, month)[1]
            
        #Find average_lowest_temprature
        min_tempr_list = [int(row['Min TemperatureC']) for row in filtered_weather_data if row['Min TemperatureC']]
        if min_tempr_list:
            monthly_results["lowest_avg_tempr"] = sum(min_tempr_list)//calendar.monthrange(year, month)[1]
        
        #Find average mean humidity
        mean_humidity_list = [int(row['Mean Humidity']) for row in filtered_weather_data if row['Mean Humidity']]
        if mean_humidity_list:
            monthly_results["avg_mean_humidity"] = sum(mean_humidity_list)//calendar.monthrange(year, month)[1]
            
        return monthly_results
    
    def get_month_temprature_readings(self, weather_data, year_month):
        year, month = map(int, year_month.split("/"))
        year_month = '{}-{}'.format(year, month)
        
        filtered_weather_data = self.filter_weather_data(weather_data, year_month)
        
        #Hold highes, lowest temprature reading for a month
        month_temprature_readings = defaultdict(lambda: None)
        
        month_temprature_readings['year_month'] = year_month
        month_temprature_readings['max_tempr'] = [int(row['Max TemperatureC']) if row['Max TemperatureC'] else None for row in filtered_weather_data]
        month_temprature_readings['min_tempr'] = [int(row['Min TemperatureC']) if row['Min TemperatureC'] else None for row in filtered_weather_data]
        
        return month_temprature_readings

obj = WeatherFilesParser()
files = obj.get_all_files("weatherfiles")
data = obj.read_weather_files(files)

print(data[0]['PKT'])

key = '2004'
[row for row in data if key in row['PKT']]