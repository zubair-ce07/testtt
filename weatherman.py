import re
import sys
import csv
import glob
import argparse

from collections import OrderedDict

from datetime import datetime


class Reporting:
    
    def __init__(self):
        pass
    
    def a_type_high_temp(self,high_temp):
        print("Highest Average : " , 
            high_temp['Mean TemperatureC'], "C")
        
    def a_type_low_temp(self,low_temp):
        print("Lowest Average : " , 
                low_temp['Mean TemperatureC'], "C")
    
    def a_type_high_humid(self, mean_humidity):
        print("Average Mean Humidity: " , 
                mean_humidity[' Mean Humidity']+ "%")

    def a_type_report(self, data):
        
        high_temp = self.extract_needed_row(
            data, 'Mean TemperatureC', True)
        low_temp = self.extract_needed_row(
            data, 'Mean TemperatureC', False)
        mean_humidity = self.extract_needed_row(
            data, ' Mean Humidity', True)
        
        self.a_type_high_temp(high_temp)
        self.a_type_low_temp(low_temp)
        self.a_type_high_humid(mean_humidity)
              
    def c_type_report(self, data):
        
        for row in data:    
            to_convert = '0' + row['Max TemperatureC']
            file_value = int(to_convert)
            print(row['PKT'], end='')
            for value in range(file_value):
                print ('\033[1;31m+\033[1;m', end = '')
            print(' ',file_value,"C")  
            
            to_convert = '0' + row['Min TemperatureC']
            file_value = int(to_convert)
            print(row['PKT'], end='')
            for value in range(file_value):
                print ('\033[1;34m+\033[1;m', end = '')
            print(' ',file_value,"C")  
            
    def e_type_report(self, data):
        
        high_temp = self.extract_needed_row(data, 'Max TemperatureC', True)
        temperature = high_temp['Max TemperatureC']
        date_to_parse = high_temp['PKT']
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Highest : " , temperature, "C",  date.strftime("%B") ,  date.day)
        
        low_temp = self.extract_needed_row(data, 'Min TemperatureC', False)
        temperature = low_temp['Min TemperatureC']
        date_to_parse = low_temp['PKT']
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Lowest : " , temperature, "C",  date.strftime("%B") ,  date.day)
        
        mean_humidity = self.extract_needed_row(data, ' Mean Humidity', True)
        temperature = mean_humidity[' Mean Humidity']
        date_to_parse = mean_humidity['PKT']
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Average Mean Humidity: " , temperature, "C",  date.strftime("%B") ,  date.day)

    def extract_needed_row(self, data, col_name, reverse_flag):
        data.sort(key=lambda x: x[col_name], reverse=reverse_flag)
        
        if not reverse_flag:
            data = [row for row in data if row[col_name] != '']
        return data[0]


def argument_handler():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-a', required=False)
    parser.add_argument('-e', required=False)
    parser.add_argument('-c', required=False)
    args = parser.parse_args()

    report = Reporting()
    if args.a:
        file_names = files_to_read('a', args.a, args.path)
        data = reading_file(file_names)
        report.a_type_report(data)
    
    if args.c:
        file_names = files_to_read('c', args.c, args.path)
        data = reading_file(file_names)
        report.c_type_report(data)
    
    if args.e:
        file_names = files_to_read('e', args.e, args.path)
        data = reading_file(file_names)
        report.e_type_report(data)
    

def reading_file(file_names):
    data = []
    for file in file_names:
         with open(file, newline='') as csvfile:
            file_data = csv.DictReader(csvfile)
            for row in file_data:
                data.append(row) 

    return data


def files_to_read(operation, file_name, file_path):
    pattren = '*{}_{}*.txt'
    
    if operation == 'a' or operation == 'c':
        file_month = datetime.strptime(file_name, "%Y/%m").strftime('%b')
        pattren = pattren.format(file_name.split('/')[0], file_month)
    elif operation == 'e':
        pattren = pattren.format(file_name, '')
    
    return glob.glob(file_path + pattren)


def main():  
    argument_handler()


if __name__ == '__main__':
    main()
