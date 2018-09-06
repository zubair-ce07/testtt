
import csv
import sys
import os
import argparse
from colorama import Fore, Back, Style


class FileParser:
    readings = [] #list of dictionary items
    months = {
	        "1" : "Jan", 
	        "2" : "Feb", 
            "3" : "Mar", 
	        "4" : "Apr", 
            "5" : "May", 
            "6" : "Jun", 
            "7" : "Jul", 
            "8" : "Aug", 
            "9" : "Sep", 
            "10" : "Oct", 
            "11" : "Nov", 
            "12" : "Dec"
	        }

    path = ""
    date = ""

    def __init__(self, path, date):
	    self.path = path
	    self.date = date
	    self.readings = []	

    def parse_file(self):	
        year = self.date.split("/")
        month = ""
        #strip 0 from left
        if (len(year) == 2):
            year[1] = year[1].lstrip("0")
            month = year[1]
		
        if (self.validateFile(year[0], month, os.listdir(self.path))):
            for file in os.listdir(self.path):
                with open(self.path+ '/'+ file) as csvfile:
                    if ((year[0] in file and len(year) == 1) or 
                        (year[0] in file and len(year) == 2 and (self.months[year[1]] in file))):
                        reader = csv.DictReader(csvfile)
                        for line in reader:
                            self.readings.append(dict(line))				
            return self.readings	
        else:
            print("File doesn't exist or incorrect arguments")
            return None	

    def validateFile(self,year, month, dir_files):
        file_substr = year

        if month:
            file_substr = file_substr+"_"+self.months[month]
        if any(file_substr in file for file in dir_files):
            return True
        else:
            return False	

			
class Calculations:
    calculation_results = {} #dictionary to hold calculation results
    file_parser = None
    path = ""
    date = ""

    def __init__(self, path, date):
        self.path = path
        self.date = date
        self.file_parser = FileParser(self.path, self.date)

    def calculations_for_command_e(self):
        parsed_readings = self.file_parser.parse_file()

        if (parsed_readings is not None):
            #Highest temperature and day
            self.calculation_results["Highest_temp"] = max([int(k["Max TemperatureC"]) for k in parsed_readings if 
                                                                k["Max TemperatureC"]])
            self.calculation_results["Highest_temp_day(s)"] = [k["PKT"] for k in parsed_readings if 
	                                                           k["Max TemperatureC"] == str(self.calculation_results["Highest_temp"])]
            #Lowest temperature and day	
            self.calculation_results["Lowest_temp"] = min([int(k["Min TemperatureC"]) for k in parsed_readings if 
                                                               k["Min TemperatureC"]]) 
            self.calculation_results["Lowest_temp_day(s)"] = [k["PKT"] for k in parsed_readings if 
                                                              k["Min TemperatureC"] == str(self.calculation_results["Lowest_temp"])]
            #Most humidity and day
            self.calculation_results["Max_humidity"] = max([int(k["Max Humidity"]) for k in parsed_readings if 
                                                                k["Max Humidity"]]) 
            self.calculation_results["Max_humidity_day(s)"] = [k["PKT"] for k in parsed_readings if 
                                                               k["Max Humidity"] == str(self.calculation_results["Max_humidity"])]
            return self.calculation_results
        else:
            return None	

    def calculations_for_command_a(self):	
        parsed_readings = self.file_parser.parse_file()

        if (parsed_readings is not None):
            #Average highest temperature
            max_temp = [int(k["Max TemperatureC"]) for k in parsed_readings if k["Max TemperatureC"]]
            self.calculation_results["Avg_highest_temp"] = int(sum(max_temp) / len(max_temp))

            #Average lowest temperature
            min_temp = [int(k["Min TemperatureC"]) for k in parsed_readings if k["Min TemperatureC"]]
            self.calculation_results["Avg_lowest_temp"] = int(sum(min_temp) / len(min_temp))

            #Average Mean Humidity
            avg_mean_humidity = [int(k[" Mean Humidity"]) for k in parsed_readings if k[" Mean Humidity"]]
            self.calculation_results["Avg_mean_humidity"] = int(sum(avg_mean_humidity) / len(avg_mean_humidity))
            return self.calculation_results

        else:	
            return None

    def calculations_for_command_c(self):
        parsed_readings = self.file_parser.parse_file()
        if (parsed_readings is not None):
            #List of Highest Temperature on each day
            self.calculation_results["Highest_temp_record"] = [k["Max TemperatureC"] for k in parsed_readings]
            #List of Lowest Temperatures on each day
            self.calculation_results["Lowest_temp_record"] = [k["Min TemperatureC"] for k in parsed_readings]
            return self.calculation_results
        else:
            return None	


class ReportGenerator:
    months = {
            "1" : "January", 
            "2" : "February", 
            "3" : "March", 
            "4" : "April", 
            "5" : "May", 
            "6" : "June", 
            "7" : "July", 
            "8" : "August", 
            "9" : "September",
            "10" : "October",
            "11" : "November",
            "12" : "December"
            }
    readings_calculator = None

    def __init__(self, path, date):
        self.path = path
        self.date = date
        self.readings_calculator = Calculations(path, date)

    #output generator for command e
    def report_generation_for_command_e(self):
        results = self.readings_calculator.calculations_for_command_e()

        if (results is not None):
            print("Highest: "+ str(results["Highest_temp"])+ "C on ", end='')
            print(','.join(str(x) for x in self.date_parser_month_day(results["Highest_temp_day(s)"])))

            print("Lowest: "+ str(results["Lowest_temp"])+ "C on ", end='')
            print(','.join(str(x) for x in self.date_parser_month_day(results["Lowest_temp_day(s)"])))

            print("Humidity: "+ str(results["Max_humidity"])+ r"% on ", end='')
            print(','.join(str(x) for x in self.date_parser_month_day(results["Max_humidity_day(s)"])))

    #output generator for command a
    def report_generation_for_command_a(self):
        readings_calculator = Calculations(self.path, self.date)
        results = readings_calculator.calculations_for_command_a()

        if (results is not None):
            print("Highest Average: "+ str(results["Avg_highest_temp"])+ "C")
            print("Lowest Average: "+ str(results["Avg_lowest_temp"])+ "C")
            print("Average Mean Humidity: "+ str(results["Avg_mean_humidity"])+ r"%")

    #output generator for command c	
    def report_generation_for_command_c(self):
        readings_calculator = Calculations(self.path, self.date)
        results = readings_calculator.calculations_for_command_c()
        count = 1
        if (results is not None):
            print(self.date_parser_year_month(self.date))
            for record_high, record_low in zip(results["Highest_temp_record"], 
                                               results["Lowest_temp_record"]): 
                print(count, end= '')
                if record_high:
                    for i in range(int(record_high)):
                        print("+", end='')
                    print()
                print(count, end= '')		
                if record_low:
                    for i in range(int(record_low)):
                        print("+", end='')
                    print()		
                count = count + 1	
        count = 0

    #date parser for month and day
    def date_parser_month_day(self, dates):
        month_description = []
        for date in dates:
            month_day = date.split("-")
            month_day[1] = month_day[1].lstrip("0")
            month_description.append(self.months[month_day[1]]+ " "+ month_day[2])
        return month_description	

    #date parser for year and month
    def date_parser_year_month(self, date):
        year_month = date.split("/")
        year_month[1] = year_month[1].lstrip("0")
        return self.months[year_month[1]]+ " "+ year_month[0] 


def main():	
    parser = argparse.ArgumentParser()
    parser.add_argument("echo", type=str, help ="Path to directory")
    parser.add_argument("-e")
    parser.add_argument("-a")
    parser.add_argument("-c")
    args = parser.parse_args()

    report = None
    if os.path.isdir(args.echo):
        if args.e:
            report = ReportGenerator(args.echo, args.e)
            report.report_generation_for_command_e()
            print()
        if args.a:
            report = ReportGenerator(args.echo, args.a)
            report.report_generation_for_command_a()	
            print()
        if args.c:
            report = ReportGenerator(args.echo, args.c)
            report.report_generation_for_command_c()
            print()	
    else:
        print("Directory does not exist !")
main()
