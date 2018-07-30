from __future__ import print_function
import os
import glob
import sys
import csv

VALID_OPTIONS = [
                    '-e','-c', '-a'
                    ]

USAGE_STRING = "Python weatherman.py [Path to weatherman files]"\
                " [Valid Options] [Valid Month, Year]"

month_names = {
                "1":"Jan", "2":"Feb",
                "3":"Mar", "4":"Apr",
                "5":"May", "6":"Jun",
                "7":"Jul", "8":"Aug",
                "9":"Sep", "10":"Oct",
                "11":"Nov", "12":"Dec"
                }


class WeatherRecord:

    def __init__(self):
        self.weather_data = None

    def read_data_from_files(self,folder_path):
        txt_files = glob.glob(folder_path+"/*.txt")  #Read text files
        self.weather_data = []
        
        for txt_file in txt_files:
            with open(txt_file, 'r') as opened_file:
                csv_reader = csv.DictReader(opened_file)
                for line in csv_reader:
                    try:
                        year_month_date = line["PKST"].split('-')
                    except KeyError:
                        year_month_date = line["PKT"].split('-')     
                    self.weather_data.append(self.populate_data(line, year_month_date))   

    def populate_data(self, data, year_month_date):
        sub_key_level_dictionary = {
                                    str(year_month_date[0]):{
                                        str(year_month_date[1]):{
                                            str(year_month_date[2]):
                                                data
                                            }
                                        }
                                    }
        return sub_key_level_dictionary
    

class ResultsCalculator:

    def __init__(self):
        self.calculated_results = {}


    def daily_temperature_calculator(self, weather_data, year, month):
        self.calculated_results = {
                                    "Month": month_names[month]
                                    ,"Year": year
                                    }
        self.calculated_results.setdefault("MaxTempreture",{})
        self.calculated_results.setdefault("MinTemperature",{})

        for data in weather_data:
            year_level_data = data.get(year)
            if year_level_data is not None:
                month_level_data = year_level_data.get(month)
                if month_level_data is not None:
                    for day in month_level_data:
                        day_level_data = month_level_data.get(day)
                        if not day_level_data.get("Max TemperatureC") == "":
                            self.calculated_results["MaxTempreture"].update({
                                str(day): day_level_data.get("Max TemperatureC")})  

                        if not day_level_data.get("Min TemperatureC") == "":
                            self.calculated_results["MinTemperature"].update({
                                str(day): day_level_data.get("Min TemperatureC")})


    def monthly_tempreture_and_humitdity_calculator(self, weather_data, year, month):
        self.calculated_results = {
                                    "HighestAverage": 0
                                    ,"LowestAverage": 0
                                    ,"AverageMeanHumidity": 0
                                    }
        total_days = 0
                                    
        for data in weather_data:    
            year_level_data = data.get(year)
            if year_level_data is not None:
                month_level_data = year_level_data.get(month)
                if month_level_data is not None:
                    for day in month_level_data:
                        total_days += 1
                        day_level_data = month_level_data.get(day)
                        if not day_level_data.get("Max TemperatureC") == "":
                            self.calculated_results["HighestAverage"] = (
                                float(day_level_data.get("Max TemperatureC")) 
                                    + float(self.calculated_results["HighestAverage"]))

                        if not day_level_data.get("Min TemperatureC") == "":
                            self.calculated_results["LowestAverage"] = (
                                float(day_level_data.get("Min TemperatureC")) 
                                    + float(self.calculated_results["LowestAverage"]))
                                                                        
                        if not day_level_data.get(" Mean Humidity") == "":
                            self.calculated_results["AverageMeanHumidity"] = (
                                float(day_level_data.get(" Mean Humidity")) 
                                    + float(self.calculated_results["AverageMeanHumidity"]))    
        
        self.calculated_results["HighestAverage"] = int(
            self.calculated_results["HighestAverage"] 
            / total_days
            )
        self.calculated_results["LowestAverage"] = int(
            self.calculated_results["LowestAverage"] 
            / total_days
            )
        self.calculated_results["AverageMeanHumidity"] = int(
            self.calculated_results["AverageMeanHumidity"] 
            / total_days
            )


    def yearly_temperature_and_humidity_calulator(self, weather_data, year):
        first_iteration = True  #Flag to memorize to do initial setup 

        for data in weather_data:
            year_level_data = data.get(year) 
            if year_level_data is not None:
                for month in year_level_data:
                    month_level_data = year_level_data.get(month)
                    for day in month_level_data:
                        temp_data  = month_level_data.get(day)
                        if first_iteration:
                            first_iteration = False
                            self.calculated_results = {
                                                        "MaxYearlyTempreature": (
                                                            temp_data.get("Max TemperatureC")
                                                            )
                                                        ,"HighestTempretureDay": day
                                                        ,"HighestTempretureMonth": (
                                                            month_names[month]
                                                            )
                                                        ,"MinYearlyTempreature": (
                                                            temp_data.get("Min TemperatureC")
                                                            )
                                                        ,"LowestTempretureDay": day
                                                        ,"LowestTempretureMonth": (
                                                            month_names[month]
                                                            )
                                                        ,"Humidity": (
                                                            temp_data.get(" Mean Humidity")
                                                            )
                                                        ,"MostHumidDay": day
                                                        ,"MostHumidMonth": (
                                                            month_names[month]
                                                            )
                                                        }
                        elif ((not temp_data.get("Max TemperatureC") == ""
                                or not temp_data.get("Min TemperatureC") == "")
                                and not temp_data.get(" Mean Humidity") ==""):

                            if (float(temp_data.get("Max TemperatureC")) 
                                    > float(self.calculated_results.get("MaxYearlyTempreature"))):
                                self.calculated_results["MaxYearlyTempreature"] = (
                                    temp_data.get("Max TemperatureC")
                                    )
                                self.calculated_results["HighestTempretureMonth"] = month_names[month]
                                self.calculated_results["HighestTempretureDay"] = day
                            elif (float(temp_data.get("Min TemperatureC"))
                                    < float(self.calculated_results.get("MinYearlyTempreature"))):
                                self.calculated_results["MinYearlyTempreature"] = (
                                    temp_data.get("Min TemperatureC")
                                    )
                                self.calculated_results["LowestTempretureMonth"] = (
                                    month_names[month]
                                    )
                                self.calculated_results["LowestTempretureDay"] = day
                            
                            if(float(temp_data.get(" Mean Humidity")) >
                                    float(self.calculated_results.get("Humidity"))):
                                self.calculated_results["Humidity"] = (
                                    temp_data.get(" Mean Humidity")
                                    )
                                self.calculated_results["MostHumidDay"]  = day
                                self.calculated_results["MostHumidMonth"] = (
                                    month_names[month]
                                    )
        

class ReportsGenrator:
    
    def __init__(self):
        pass

    def yearly_report_genrator(self, calculated_results):
        print("Highest: " + calculated_results["MaxYearlyTempreature"]\
                +"C on " + calculated_results["HighestTempretureDay"]\
                +" " + calculated_results["HighestTempretureMonth"])
        print("Lowest: " + calculated_results["MinYearlyTempreature"]\
                +"C on " + calculated_results["LowestTempretureDay"]\
                +" " + calculated_results["LowestTempretureMonth"])
        print("Humidity: " + calculated_results["Humidity"]\
                +"% on " + calculated_results["MostHumidDay"]\
                +" " + calculated_results["MostHumidMonth"])
    

    def monthly_report_genrator(self, calculated_results):
        print("Highest Average: " 
                + str(calculated_results["HighestAverage"]) + "C")
        print("Lowest Average: " 
                + str(calculated_results["LowestAverage"]) + "C")
        print("Average Mean Humidity: " 
                + str(calculated_results["AverageMeanHumidity"]) + "%")

    

    def daily_report_genrator(self, calculated_results, caller_flag):
        print(calculated_results["Month"] 
                +" "+ calculated_results["Year"])
        daily_max_data = calculated_results.get("MaxTempreture")
        daily_min_data = calculated_results.get("MinTemperature")

        if caller_flag:  #Called from daily calculator
            for day in zip(daily_max_data, daily_min_data):
                print(day[0], end="")
                for iterator in range(0, int(daily_max_data.get(day[0]))):
                    sys.stdout.write("\033[1;31m")  #Red color
                    print("+", end="")
                    sys.stdout.write("\033[1;00m")  #White
                print(" " + daily_max_data.get(day[0]) + "C")
                print(day[0], end="")
                for iterator in range(0, int(daily_min_data.get(day[0]))):
                    sys.stdout.write("\033[1;34m")  #Blue color
                    print("+", end="")
                    sys.stdout.write("\033[1;00m")  #White
                print(" " + daily_min_data.get(day[0]) + "C")

        else:

            for day in zip(daily_max_data, daily_min_data):
                print(day[0], end="")
                for iterator in range(0, int(daily_min_data.get(day[0]))):
                    sys.stdout.write("\033[1;34m")  #Blue color
                    print("+", end="")
                    sys.stdout.write("\033[1;00m")  #White

                for iterator in range(0, int(daily_max_data.get(day[0]))):
                    sys.stdout.write("\033[1;31m")  #Red color
                    print("+", end="")
                    sys.stdout.write("\033[1;00m")  #White
                print(" " + daily_min_data.get(day[0]) + "C", end="")
                print(" - " + daily_max_data.get(day[0]) + "C")


def usage_printer():
    print("Usage:")
    print(USAGE_STRING)
    print("Options:")
    print(VALID_OPTIONS)
    sys.exit()


def yearly_calculator_n_genrator_caller(ResultsCalculatorInstance, year):
    ResultsCalculatorInstance.yearly_temperature_and_humidity_calulator(
        WeatherRecordInstance.weather_data, year
        )
    ReportsGenratorInstance.yearly_report_genrator(
        ResultsCalculatorInstance.calculated_results
        )


def monthly_calculator_n_genrator_caller(ResultsCalculatorInstance, year, month):
    ResultsCalculatorInstance.monthly_tempreture_and_humitdity_calculator(
        WeatherRecordInstance.weather_data, year,
        month
        )
    ReportsGenratorInstance.monthly_report_genrator(
        ResultsCalculatorInstance.calculated_results
        )
    ResultsCalculatorInstance.daily_temperature_calculator(
        WeatherRecordInstance.weather_data,
        year, month
        )
    ReportsGenratorInstance.daily_report_genrator(
        ResultsCalculatorInstance.calculated_results,
        False
        )

def daily_calculator_n_genrator_caller(ResultsCalculatorInstance, year, month):
    ResultsCalculatorInstance.daily_temperature_calculator(
        WeatherRecordInstance.weather_data,
        year, month
        )
    ReportsGenratorInstance.daily_report_genrator(
        ResultsCalculatorInstance.calculated_results,
        True
        )


if __name__ == "__main__":

    if sys.argv[2] not in VALID_OPTIONS:  #Verify valid options
        print("Invalid Option")
        usage_printer()
    
    if not os.path.isdir(sys.argv[1]):  #Verify valid files path  
        print("Invalid Path")
        usage_printer()
    
    WeatherRecordInstance = WeatherRecord()
    WeatherRecordInstance.read_data_from_files(sys.argv[1])
    
    ResultsCalculatorInstance = ResultsCalculator()

    ReportsGenratorInstance = ReportsGenrator()

    if len(sys.argv) > 3:  #Multiple reports
        for iterator in range(0, len(sys.argv)):
            if sys.argv[iterator] == '-a':
                splited_year_n_month = sys.argv[iterator+1].split("/")  #Parse input
                monthly_calculator_n_genrator_caller(ResultsCalculatorInstance, 
                                                    splited_year_n_month[0], 
                                                    splited_year_n_month[1])
            
            if sys.argv[iterator] == '-c':
                splited_year_n_month = sys.argv[iterator+1].split("/")  #Parse input
                splited_year_n_month[1] = splited_year_n_month[1].replace("0","")
                daily_calculator_n_genrator_caller(ResultsCalculatorInstance, 
                                                    splited_year_n_month[0], 
                                                    splited_year_n_month[1])
            
            if sys.argv[iterator] == '-e':
                yearly_calculator_n_genrator_caller(ResultsCalculatorInstance,
                                                    str(sys.argv[iterator+1]))

    else:
        if sys.argv[2] == '-a':
            splited_year_n_month = sys.argv[3].split("/")  #Parse input
            monthly_calculator_n_genrator_caller(ResultsCalculatorInstance, 
                                                splited_year_n_month[0], 
                                                splited_year_n_month[1])
        elif sys.argv[2] == '-c':
            splited_year_n_month = sys.argv[3].split("/")  #Parse input
            daily_calculator_n_genrator_caller(ResultsCalculatorInstance, 
                                                splited_year_n_month[0], 
                                                splited_year_n_month[1])
        elif sys.argv[2] == '-e':
            yearly_calculator_n_genrator_caller(ResultsCalculatorInstance, 
                                                str(sys.argv[3]))