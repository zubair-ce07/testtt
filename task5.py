import copy
import csv
import sys
import os
from read_file import read_file 
from data import data


class task5(data):
    def task(self,month,year):
        read_file.read_one_month(self.month_check[month], str(year),self.list_month,
                                 self.list_year,self.dic,self.day)
        RED = "\033[1;31m"
        BLUE = "\033[1;34m"
        RESET = "\033[0;0m"
        if self.day is not None:
            for data in self.day:
                print(data["PKT"], end='')
                # min temp
                max_temp = data["Max TemperatureC"]
                min_tmep = data["Min TemperatureC"]
                sys.stdout.write(BLUE)
                if min_tmep != "":
                    for count in range(int(min_tmep)):
                        print("+", end="")
                    # max temp
                    max_temp = data["Max TemperatureC"]
                else:
                    sys.stdout.write(RESET)
                    print(" None")
                sys.stdout.write(RED)
                if max_temp != "":
                    for count in range(int(max_temp)):
                        print("+", end="")
                    sys.stdout.write(RESET)
                    print(" ", min_tmep, "C", end=" ")
                    print(" ", max_temp, "C")
                sys.stdout.write(RESET)
        else:
            print("NO data found")
