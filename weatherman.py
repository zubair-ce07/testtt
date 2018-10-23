import re
import sys
import csv
import glob
import argparse

from collections import OrderedDict
from datetime import datetime


class Reporting:

    def a_type_report(self, data):
        high_temp = self.needed_row(data, 'Mean TemperatureC', True)
        print("Highest Average : " , high_temp['Mean TemperatureC'], "C")

        low_temp = self.needed_row(data, 'Mean TemperatureC', False)
        print("Lowest Average : " , low_temp['Mean TemperatureC'], "C")
        
        mean_humidity = self.needed_row(data, ' Mean Humidity', True)
        print("Average Mean Humidity: " , mean_humidity[' Mean Humidity']+ "%")
              
    def c_type_report(self, data):
        
        for row in data:
            if row['Max TemperatureC'] != '':
                to_convert = row['Max TemperatureC']
                file_value = int(to_convert)
                print(row['PKT'], end='')
                for value in range(file_value):
                    print ('\033[1;31m+\033[1;m', end = '')
                print(' ',file_value,"C")  
            
            if row['Min TemperatureC'] != '':
                to_convert = row['Min TemperatureC']
                file_value = int(to_convert)
                print(row['PKT'], end='')
                for value in range(file_value):
                    print ('\033[1;34m+\033[1;m', end = '')
                print(' ',file_value,"C")  
            
    def e_type_report(self, data):
        
        high_temp = self.needed_row(data, 'Max TemperatureC', reverse_flag=True)
        temperature = high_temp['Max TemperatureC']
        if 'PKT' in high_temp:
            key = 'PKT'
        else:
            key = 'PKST'
        date_to_parse = high_temp.get(key)
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Highest : ", temperature, "C", date.strftime("%B"), date.day)
        
        low_temp = self.needed_row(data, 'Min TemperatureC', reverse_flag=False)
        temperature = low_temp['Min TemperatureC']
        if 'PKT' in high_temp:
            key = 'PKT'
        else:
            key = 'PKST'
        date_to_parse = high_temp.get(key)
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Lowest : ", temperature, "C", date.strftime("%B"), date.day)
        
        mean_humidity = self.needed_row(data, ' Mean Humidity', reverse_flag=True)
        temperature = mean_humidity[' Mean Humidity']
        if 'PKT' in high_temp:
            key = 'PKT'
        else:
            key = 'PKST'
        date_to_parse = high_temp.get(key)
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Average Mean Humidity: ", temperature, "C", date.strftime("%B"), date.day)

    def needed_row(self, data, col_name, reverse_flag):
        data = [row for row in data if row[col_name] != '']
        
        data.sort(key=lambda x: int(x[col_name]), reverse=reverse_flag)
        return data[0]

    
def reading_file(file_names):
    data = []
    for file in file_names:
         with open(file, newline='') as csvfile:
            file_data = csv.DictReader(csvfile)
            for row in file_data:
                data.append(row) 
    return data


def file_name(operation, file_name, file_path):
    pattren = '*{}_{}*.txt'
    
    if operation == 'a' or operation == 'c':
        file_month = datetime.strptime(file_name, "%Y/%m").strftime('%b')
        pattren = pattren.format(file_name.split('/')[0], file_month)
    elif operation == 'e':
        pattren = pattren.format(file_name, '')
    
    return glob.glob(file_path + pattren)


def main():  
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-a', required=False)
    parser.add_argument('-e', required=False)
    parser.add_argument('-c', required=False)
    args = parser.parse_args()

    report = Reporting()
    if args.a:
        file_names = file_name('a', args.a, args.path)
        if file_names:
            data = reading_file(file_names)
            report.a_type_report(data)
        else:
            print('File may not be available against -a argument!')  
    
    if args.c:
        file_names = file_name('c', args.c, args.path)
        if file_names:
            data = reading_file(file_names)
            report.c_type_report(data)
        else:
            print('File may not be available against -c argument!')
    
    if args.e:
        file_names = file_name('e', args.e, args.path)
        if file_names:
            data = reading_file(file_names)
            report.e_type_report(data)
        else:
            print('File may not be available against -e argument!')


if __name__ == '__main__':
    main()
