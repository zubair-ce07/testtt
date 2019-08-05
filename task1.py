import copy
import csv
import sys
import os
from read_file import read_file 
from data import data 

class task1(data):

    def task(self,year):
        read_file.read_year(year,self.list_month,self.list_year,self.day,self.month_check,self.dic)
        Max_TemperatureC = -999999
        Max_TemperatureC_Day = None
        Min_TemperatureC = 999999
        Min_TemperatureC_Day = None
        Max_Humidity = -99999
        Max_Humidity_Day = None

        for year in range(12):
            if self.list_month[year] is not None:
                for data in self.list_month[year]:
                    if data["Max TemperatureC"] != '':
                        if Max_TemperatureC < int(data["Max TemperatureC"]):
                            Max_TemperatureC = int(data["Max TemperatureC"])
                            Max_TemperatureC_Day = data["PKT"]
                    if data["Min TemperatureC"] != '':
                        if Min_TemperatureC > int(data["Min TemperatureC"]):
                            Min_TemperatureC = int(data["Min TemperatureC"])
                            Min_TemperatureC_Day = data["PKT"]
                    if data["Max Humidity"] != '':
                        if Max_Humidity < int(data["Max Humidity"]):
                            Max_Humidity = int(data["Max Humidity"])
                            Max_Humidity_Day = data["PKT"]

        print(Max_TemperatureC, "C ", Max_TemperatureC_Day)
        print(Min_TemperatureC, "C ", Min_TemperatureC_Day)
        print(Max_Humidity, "% ", Max_Humidity_Day)
    