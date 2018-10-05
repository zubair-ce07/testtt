import re
import sys
import csv
import glob
import datetime
import argparse


class Reporting:
    
    def __init__(self, operation, complete_data):
        if operation == 'a':
            self.a_type_report(complete_data)
        elif operation == 'c':
            self.c_type_report(complete_data)
        elif operation == 'e':
            self.e_type_report(complete_data)

    def a_type_report(self, complete_data):

        year_key = list(complete_data.keys())[0]
        days_key = list(complete_data[year_key].keys())
        
        high_temp = 0
        days_count = 0
        for days in days_key:
            try:
                file_value = int(complete_data[year_key][days]['Max TemperatureC'])
                high_temp += file_value
                days_count += 1
                    
            except:
                pass
        print("Highest Average : " , round(high_temp/days_count, 2), "C")

        low_temp = 0
        days_count = 0
        for days in days_key:
            try:
                file_value = int(complete_data[year_key][days]['Min TemperatureC'])
                low_temp += file_value
                days_count += 1
                
            except:
                pass
        print("Lowest Average : " , round(low_temp/days_count, 2), "C")

        mean_humid = 0
        days_count = 0
        for days in days_key:
            try:
                file_value = int(complete_data[year_key][days][' Mean Humidity'])
                mean_humid += file_value
                days_count += 1
                
            except:
                pass
        print("Average Mean Humidity: " , str(int(mean_humid/days_count))+ "%")

    def c_type_report(self, complete_data):
        year_key = list(complete_data.keys())[0]
        days_key = list(complete_data[year_key].keys())
        
        for days in days_key:
            try:
                file_value = int(complete_data[year_key][days]['Max TemperatureC'])
                print(days, end='')
                for value in range(file_value):
                    print ('\033[1;31m+\033[1;m', end = '')
                print(file_value,"C")  
            except:
                continue
            
            try:
                file_value = int(complete_data[year_key][days]['Min TemperatureC'])
                print(days, end='')
                for value in range(file_value):
                    print ('\033[1;34m+\033[1;m', end = '')
                print(file_value,"C")  
            except:
                continue

    def e_type_report(self, complete_data):
        [value, month, day] = self.find_max_temp(complete_data)
        print("Highest:", value, "C on", month, day)
        [value, month, day] = self.find_min_temp(complete_data)
        print("Lowest:", value, "C on", month, day)
        [value, month, day] = self.find_max_humid(complete_data)
        print("Humidity:", value, "% on", month, day)

    def find_max_temp(self, complete_data):
        year_keys = list(complete_data.keys())
        
        max_temp_value = 0
        for year_key in year_keys:
            day_keys = list(complete_data[year_key].keys())
            
            for day_key in day_keys:
                try:
                    file_value = int(complete_data[year_key][day_key]['Max TemperatureC'])
                    if max_temp_value < file_value:
                        max_temp_value = file_value
                        high_month_key = year_key
                        high_day_key = day_key
                except:
                    continue    

        return [max_temp_value, high_month_key[5:], high_day_key]

    def find_min_temp(self, complete_data):
        year_keys = list(complete_data.keys())
        
        min_temp_value = 0
        for year_key in year_keys:
            day_keys = list(complete_data[year_key].keys())
            
            for day_key in day_keys:
                try:
                    file_value = int(complete_data[year_key][day_key]['Min TemperatureC'])
                    if min_temp_value >= file_value:
                        min_temp_value = file_value
                        low_month_key = year_key
                        low_day_key = day_key
                except:
                    continue

        return [min_temp_value, low_month_key[5:], low_day_key]

    def find_max_humid(self, complete_data):
        year_keys = list(complete_data.keys())
        
        max_temp_value = 0
        for year_key in year_keys:
            day_keys = list(complete_data[year_key].keys())
            
            for day_key in day_keys:
                try:
                    file_value = int(complete_data[year_key][day_key]['Max Humidity'])
                    if max_temp_value < file_value:
                        max_temp_value = file_value
                        high_month_key = year_key
                        high_day_key = day_key
                except:
                    continue    

        return [max_temp_value, high_month_key[5:], high_day_key]


def argument_handler():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-a', required=False)
    parser.add_argument('-e', required=False)
    parser.add_argument('-c', required=False)
    args = parser.parse_args()

    if args.a:
        reading_file(args.path, 'a', args.a)
    if args.e:
        reading_file(args.path, 'e', args.e)
    if args.c:
        reading_file(args.path, 'c', args.c)


def file_to_read_list(operation, file_name, file_path):
    if operation == 'a' or operation == 'c':
        file_name,month = file_name.split('/')
        pattren = "*"+ file_name +"_"\
                +datetime.date(int(file_name), int(month), 1).strftime('%b')\
                + "*.txt"
    elif operation == 'e':
        pattren = "*"+ file_name + "*.txt"
    
    return glob.glob(file_path + pattren)


def reading_file(file_path, operation, file_name):
    
    file_to_read = file_to_read_list(operation, file_name, file_path)
    complete_data = {}
    for file in file_to_read:
        with open(file, newline='') as csvfile:
            file_data = list(csv.reader(csvfile))
            file_headers = file_data[0]
            file_data = file_data[1:-1]
            
            days_data = {}
            days_count = 1
            for day in file_data:
                index = 0
                row = {}
                for col_name in file_headers:
                    row.update({col_name : day[index]})
                    index += 1
                days_data.update({days_count:row})
                days_count += 1
                row = {}
        complete_data.update({file[-12:-4]:days_data})

    Reporting(operation, complete_data)
    

def main():  
    argument_handler()


if __name__ == '__main__':
    main()
