#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:39:49 2019

@author: abdullah
"""

import csv
import glob
import datetime
import argparse


class Reader:

    def filesread(self):
        
        alldata = []
        for f in glob.glob("/home/abdullah/Downloads/weatherfiles/*.txt"):
            for record in csv.DictReader(open(f)):
                if(record.get("PKT") or record.get("PKST")) and record.get("Max TemperatureC") and \
                record.get("Min TemperatureC") and record.get("Max Humidity") and record.get(" Mean Humidity") \
                and record.get("Mean TemperatureC") and record.get(" Min Humidity"):                    
                    alldata.append(StoreRecord(record))
        
        return alldata
    

class StoreRecord:

    def __init__(self, record):   
        
        date = record.get("PKT") or record.get("PKST")
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.max_temp = int(record.get("Max TemperatureC"))
        self.min_temp = int(record.get("Min TemperatureC"))
        self.max_humidity = int(record.get("Max Humidity"))
        self.mean_humidity = int(record.get(" Mean Humidity")) 
        self.mean_temp = int(record.get("Mean TemperatureC"))
        self.min_humidity = int(record.get(" Min Humidity"))


class Calculator: 

    def avg_cal(self, alldata, input_date):
        
        records = [record for record in alldata if record.date.year == input_date.year and \
                  record.date.month == input_date.month]         
        avg_max_temp = sum([item.max_temp for item in records]) / len(records)
        avg_min_temp = sum([item.min_temp for item in records]) / len(records)
        avg_mean_humidity = sum([item.max_humidity for item in records]) / len(records)
       
        return avg_max_temp, avg_min_temp, avg_mean_humidity

    def temps(self, alldata, input_date):
        
        records = [record for record in alldata if record.date.year == input_date.year]
        max_temp = max(records, key=lambda item: item.max_temp)
        min_temp = max(records, key=lambda item: item.min_temp)
        max_humidity = max(records, key=lambda item: item.max_humidity) 
        
        return max_temp, min_temp, max_humidity
    
    def graphrecords(self, alldata, input_date):
        
        records = [record for record in alldata if record.date.year == input_date.year \
                   and record.date.month == input_date.month]
        
        maxtemp = [item.max_temp for item in records]
            
        mintemp = [item.min_temp for item in records]
        
        return maxtemp,mintemp
    
class Generator:
    
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
       
    def gen_avgs(self, avg_max_temp, avg_min_temp, avg_mean_humidity):
        
        print("REPORT 2")
        print(f'Average maximum temperature: {avg_max_temp}C')
        print(f'Average minimum temperature: {avg_min_temp}C')
        print(f'Average mean humidity: {avg_mean_humidity}%')
        
        
    def gen_maxs(self, max_temp, min_temp, max_humidity):
        
        print("REPORT 1")
        print(f'maximum temperature: {max_temp.max_temp}C on {max_temp.date: %B} {max_temp.date: %d}')
        print(f'minimum temperature: {min_temp.min_temp}C on {min_temp.date: %B} {min_temp.date: %d}')
        print(f'humidity: {max_humidity.max_humidity}% on {max_humidity.date: %B} {max_humidity.date: %d}')            
        
    def graph(self, maxtemp, mintemp, input_date):
        
        print("REPORT 3")
        print(f'{input_date: %B} {input_date.year}')
        
        a=1
        b=1
        
        for i,j in zip(maxtemp, mintemp):
            
            print(Generator.FAIL + str(a) + i*'+' + str(i))
            a +=1
            print(Generator.OKBLUE + str(b) + j*'+' + str(j))
            b +=1

    

def main():
    
    s1 = Reader()
    s2 = Calculator()
    s3 = Generator()
    d = s1.filesread()
    #print(d)
    parser = argparse.ArgumentParser()
    parser.add_argument("yearlytemp", help="Input year here for max min temp")
    parser.add_argument("avgtempmonth", help="Input year and month for average of month")
    parser.add_argument("graphyear", help="Input year and month for graph here")
    args = parser.parse_args()
    
    yearnmonth = datetime.datetime.strptime(args.avgtempmonth, '%Y/%m').date() 
    year = datetime.datetime.strptime(args.yearlytemp, '%Y').date()
    graphyear = datetime.datetime.strptime(args.graphyear, '%Y/%m').date()
    
    if args.yearlytemp:
        max_temp,mintemp,max_humidity = s2.temps(d, year)
       
    
    s3.gen_maxs(max_temp, mintemp, max_humidity)
    
    if args.avgtempmonth:
        avg_max_temp,avg_min_temp,avg_mean_humidity = s2.avg_cal(d, yearnmonth)
        
    s3.gen_avgs(avg_max_temp, avg_min_temp, avg_mean_humidity)
    
    if args.graphyear:
        maxtemp,mintemp = s2.graphrecords(d, graphyear)
        
    s2.graphrecords(d, graphyear)
    
    s3.graph(maxtemp,mintemp, graphyear) 
    
    
    
    
    
    
        
    
if __name__ == '__main__':
    main()
    

    
    
