import os
import csv
import glob
from datetime import datetime


class WeatherAnalysis:
    
    def __init__(self, weather_reading):
        if weather_reading:
            if weather_reading['PKT']:
                self.full_date = weather_reading['PKT'] 
                self.date_split = weather_reading['PKT'].split('-')
                self.day = int(self.date_split[2])
            if weather_reading['Max TemperatureC']:
                self.max_temp = int(weather_reading['Max TemperatureC'])
            
            if weather_reading['Min TemperatureC']:
                self.min_temp = int(weather_reading['Min TemperatureC'])
            if weather_reading[' Mean Humidity']:
                self.mean_humidity = int(weather_reading[' Mean Humidity'])
            if weather_reading['Max Humidity']:
                self.max_humidity = int(weather_reading['Max Humidity'])

        
class WeatherReport:
    def __init__(self):
        print('')

    def display_month_bar_chart(self, file_data):
         
        for data_row in file_data:
            max_value = data_row.max_temp
            min_value = data_row.min_temp
            date = data_row.day
            print(date, end="")
            for value in range(max_value):
                print("\033[1;31m+\033[1;m", end="")
            
            if min_value < 0:
                for value in range(abs(min_value)):
                    print("\033[1;34m-\033[1;m", end="")
                    
            for value in range(min_value):
                print("\033[1;34m+\033[1;m", end="")
            print(max_value, end="")
            print("C- ", end="")
            print(min_value, end="")
            print("C")

    def display_monthly_report(self, file_data):
        high_temp = self.get_max_temp(file_data)
        print("Highest Average : {}C".format(high_temp))

        low_temp = self.get_min_temp(file_data)
        print("Lowest Average : {}C".format(low_temp))

        mean_humidity = int(self.get_mean_humidity(file_data))
        print("Average Mean Humidity : {}% ".format(mean_humidity))

    def display_month_chart_report(self, file_data):
        self.file_data = file_data
        for file_row in file_data:
            
                max_value = file_row.max_temp
                min_value = file_row.min_temp
                get_day = file_row.day
                print(get_day, end="")
                for max_temp_count in range(max_value):
                    print("\033[1;31m+\033[1;m", end="")
                print(" ", max_value, "C")
                get_day = file_row.day
                print(get_day, end="")
                if min_value < 0:
                    for min_temp_count in range(abs(min_value)):
                        print("\033[1;34m-\033[1;m", end="")
                    print(" {}C".format(min_value))
                else:
                    for min_temp_count in range(min_value):
                        print("\033[1;34m+\033[1;m", end="")
                    print(" {}C".format(min_value))
        
    def display_yearly_report(self, file_data):
        high_temp = self.get_max_average(file_data)
        date = self.get_required_date(file_data,file_data.high_temp,reverse_flag=True)
        print("Highest: {}C on {} {}".format(high_temp,date.strftime("%B"),date.day))
        
        date = self.get_required_date(file_data,file_data.min_temp,reverse_flag=False)
        low_temp = self.get_min_average(file_data)
        print("Lowest: {}C on {} {}".format(low_temp,date.strftime("%B"),date.day))

        date = self.get_required_date(file_data,file_data.average_humidity,reverse_flag=True)
        mean_humidity = self.get_mean_humidity(file_data)
        print("Humidity: {} on {} {}%".format(mean_humidity,date.strftime("%B"),date.day))

    def get_max_temp(self, file_data):
        max_list = []
        for file_rows in file_data:
            if file_rows.max_temp !='' or not file_rows:
                max_list.append(file_rows.max_temp)
            
        return max(max_list)

    def get_min_temp(self, file_data):
        min_list = []
        for file_rows in file_data:
            min_list.append(file_rows.min_temp)
            
        return min(min_list)

    def get_mean_humidity(self, file_data):
        mean_list = []
        for file_rows in file_data:
            mean_list.append(file_rows.max_temp)
            
        return (sum(mean_list)/len(mean_list))
    
    def get_max_average(self, file_data):
        mean_list_max = []
        
        for file_rows in file_data:
            mean_list_max.append(file_rows.max_temp)
            
        return (sum(mean_list_max)/len(mean_list_max))

    def get_min_average(self, file_data):
        mean_list_min = []
        for file_rows in file_data:
            mean_list_min.append(file_rows.min_temp)
            
        return (sum(mean_list_min)/len(mean_list_min))    

    def get_required_date(self, file_data,required_value,reverse_flag):
        file_data = [file_row.full_date for file_row in file_data if required_value ]
        file_data.sort(key=lambda x: int(required_value), reverse=reverse_flag)
        return file_data[0]

class FileData:
    def reading_file(self,file_names):
        weather_readings = []
        for file_name in file_names:
            with open(file_name, 'r') as csvfile:
                weather_file_readings = csv.DictReader(csvfile)
                
                for row in weather_file_readings:
                    weather_readings.append(WeatherAnalysis(row)) 
                   
        return weather_readings            
        


    def get_file_name(self,arguments, file_name, file_path):
        pattern = "*{}_{}*.txt"

        if arguments == "a" or arguments == "c":
            file_month = datetime.strptime(file_name, "%Y/%m").strftime("%b")
            pattern = pattern.format(file_name.split("/")[0], file_month)
        elif arguments == "e":
            pattern = pattern.format(file_name, "")

        return glob.glob(file_path + pattern)


        



