import re
import sys
import csv
import glob
import argparse

from datetime import datetime


class Reporting:
    
    def __init__(self):
        pass
    
    def a_type_high_temp(self,high_temp, head):
        
        print("Highest Average : " , 
            high_temp[head.index('Max TemperatureC')], "C")
        
    def a_type_low_temp(self,low_temp, head):
        print("Lowest Average : " , 
                low_temp[head.index('Min TemperatureC')], "C")
    
    def a_type_high_humid(self, mean_humidity, head):
        print("Average Mean Humidity: " , 
                mean_humidity[head.index(' Mean Humidity')]+ "%")

    def a_type_report(self, complete_data):
        head = complete_data['header']
        
        high_temp = self.extract_needed_row(
            complete_data, 'Mean TemperatureC', True)
        low_temp = self.extract_needed_row(
            complete_data, 'Mean TemperatureC', False)
        mean_humidity = self.extract_needed_row(
            complete_data, ' Mean Humidity', True)
        
        self.a_type_high_temp(mean_humidity, head)
        self.a_type_low_temp(low_temp, head)
        self.a_type_high_humid(high_temp, head)
        
        
    def c_type_report(self, complete_data):
        head = complete_data['header']
        data = complete_data['data']
        max_index = head.index('Max TemperatureC')
        min_index = head.index('Min TemperatureC')
        day_index = head.index('PKT')
        
        for row in data:    
            to_convert = '0' + row[max_index]
            file_value = int(to_convert)
            print(row[day_index], end='')
            for value in range(file_value):
                print ('\033[1;31m+\033[1;m', end = '')
            print(' ',file_value,"C")  
            
            to_convert = '0' + row[min_index]
            file_value = int(to_convert)
            print(row[day_index], end='')
            for value in range(file_value):
                print ('\033[1;34m+\033[1;m', end = '')
            print(' ',file_value,"C")  
            
    def e_type_report(self, complete_data):
        head = complete_data['header']
        
        high_temp = self.extract_needed_row(complete_data, 'Max TemperatureC', True)
        temperature = high_temp[head.index('Max TemperatureC')]
        date_to_parse = high_temp[head.index('PKT')]
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Highest : " , temperature, "C",  date.strftime("%B") ,  date.day)
        
        low_temp = self.extract_needed_row(complete_data, 'Min TemperatureC', False)
        temperature = low_temp[head.index('Min TemperatureC')]
        date_to_parse = low_temp[head.index('PKT')]
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Lowest : " , temperature, "C",  date.strftime("%B") ,  date.day)
        
        mean_humidity = self.extract_needed_row(complete_data, ' Mean Humidity', True)
        temperature = mean_humidity[head.index(' Mean Humidity')]
        date_to_parse = mean_humidity[head.index('PKT')]
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Average Mean Humidity: " , temperature, "C",  date.strftime("%B") ,  date.day)

    def extract_needed_row(self, complete_data, col_name, reverse_flag):
        head = complete_data['header']
        data = complete_data['data']
        temp_index = head.index(col_name)
        data.sort(key=lambda x: x[temp_index], reverse=reverse_flag)
        if not reverse_flag:
            data = [row for row in data if row[temp_index] != '']
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
        complete_data = reading_file(file_names)
        report.a_type_report(complete_data)
    
    if args.c:
        file_names = files_to_read('c', args.c, args.path)
        complete_data = reading_file(file_names)
        report.c_type_report(complete_data)
    
    if args.e:
        file_names = files_to_read('e', args.e, args.path)
        complete_data = reading_file(file_names)
        report.e_type_report(complete_data)
    

def reading_file(file_names):
    data = []
    for file in file_names:
         with open(file, newline='') as csvfile:
            file_data = csv.reader(csvfile)
            header = next(file_data)
            for row in file_data:
                data.append(row) 
    
    complete_data = {'header': header, 'data':data}
    return complete_data


def files_to_read(operation, file_name, file_path):
    if operation == 'a' or operation == 'c':
        file_name += '/1'
        pattren = "*" + file_name.split('/')[0] + "_"\
                + datetime.strptime(file_name, "%Y/%m/%d").strftime('%b')\
                + "*.txt"
    elif operation == 'e':
        pattren = "*"+ file_name + "*.txt"
    return glob.glob(file_path + pattren)


def main():  
    argument_handler()


if __name__ == '__main__':
    main()
