import argparse
import os
import csv
import sys
import itertools

from operator import itemgetter
from datetime import datetime


class Record_File:
    """
    This class will work to read a file from directory and hold records
    """

    
    def __init__(self):
        self.weather_records = []   
        
    def read_file(self):
        filenames = [f for f in os.listdir('.')
                    if os.path.isfile(os.path.join('.', f)) and f.endswith('.txt')]
        for entry in filenames:
            with open(entry, "r") as file_open:
                fileread = csv.reader(file_open)
                keys = fileread.__next__()
                for row in fileread:
                    self.weather_records.append(dict(zip(keys,row)))
        
                file_open.close()

                
class yearly_computing_results:
    """
    This class takes the objects from list and computing yearly results
    """


    def getting_yearly_objects(self,record,year):
        calculating_records = []
        for index in range(len(record)):
            for key in record[index]:        
                if(record[index][key].startswith(year)):
                    calculating_records.append(record[index])

        return calculating_records

    def gethighesttemperature(self,req_objects):
        max_temperature = [ sub['Max TemperatureC'] for sub in req_objects]
        max_temp = list(map(int, max_temperature))
        pkt = [ sub['PKT'] for sub in req_objects] or [ sub['PKST'] for sub in req_objects]
        merge = list(zip(max_temp,pkt))
        result = max(merge,key=itemgetter(0))
        print("Highest Temperature And Day: ", result)

    def getlowesttemperature(self,req_objects):
        min_temperature = [ sub['Min TemperatureC'] for sub in req_objects]
        min_temp = list(map(int, min_temperature))
        pkt = [ sub['PKT'] for sub in req_objects] or [ sub['PKST'] for sub in req_objects]
        merge = list(zip(min_temp,pkt))
        result = min(merge,key=itemgetter(0))
        print("Lowest Temperature And Day: ", result)

    def gethighesthumidity(self,req_objects):
        max_humidity = [ sub['Max Humidity'] for sub in req_objects]
        max_humid = list(map(int, max_humidity))
        pkt = [ sub['PKT'] for sub in req_objects] or [ sub['PKST'] for sub in req_objects]
        merge = list(zip(max_humid,pkt))
        result = min(merge,key=itemgetter(0))
        print("Max Humidity And Day: ", result)
        
            
class monthly_computing_results:
    """
    This class takes the objects from list and computing monthly results
    """


    def getting_monthly_objects(self,record,year,month):
        calculating_records = []

        for index in range(len(record)):
            for key in record[index]:        
                if(record[index][key].startswith(year + '-' + month)):
                    calculating_records.append(record[index])
        
        return calculating_records

    def getmaximumaverage(self,req_objects):
        row_count = sum(1 for row in req_objects)
        max_temperature = [ sub['Max TemperatureC'] for sub in req_objects]
        convert_list = list(map(int, max_temperature))
        sum_of_max_temperature = sum(convert_list)
        average = int(sum_of_max_temperature) / row_count
        print("Maximum Average Temperature:", int(average), "C")

    def getminimumaverage(self,req_objects):
        row_count = sum(1 for row in req_objects)
        min_temperature = [ sub['Min TemperatureC'] for sub in req_objects]
        convert_list = list(map(int, min_temperature))
        sum_of_min_temperature = sum(convert_list)
        average = int(sum_of_min_temperature) / row_count
        print("Minimum Average Temperature:", int(average), "C")

    def gethumidityaverage(self,req_objects):
        row_count = sum(1 for row in req_objects)
        mean_humidty = [ sub[' Mean Humidity'] for sub in req_objects]
        convert_list = list(map(int, mean_humidty))
        sum_of_mean_humidity = sum(convert_list)
        average = int(sum_of_mean_humidity) / row_count
        print("Mean Humidity Average:", int(average), "%")
    

class monthly_report:
    """
    This class takes the objects from list and draw multiline chart on console
    """


    def getting_monthly_objects(self,record,year,month):
        calculating_records = []
        for index in range(len(record)):
            for key in record[index]:        
                if(record[index][key].startswith(year + '-' + month)):
                    calculating_records.append(record[index])

        return calculating_records
    
    def monthly_chart(self,req_objects):
        COLOR_BLUE = '\033[1;34;48m'
        COLOR_RED = '\033[1;31;48m'
        
        max_temperature = [ sub['Max TemperatureC'] for sub in req_objects]
        max_temp_convert_list = list(map(int, max_temperature))
        min_temperature = [ sub['Min TemperatureC'] for sub in req_objects]
        min_temp_convert_list = list(map(int, min_temperature))
        pkt = [ sub['PKT'] for sub in req_objects] or [ sub['PKST'] for sub in req_objects]

        for pkt,max_temp,min_temp in zip(pkt,max_temp_convert_list,min_temp_convert_list):
            print(f"{pkt}{COLOR_RED.format('+' * max_temp)}{max_temp}C")
            print(f"{pkt}{COLOR_BLUE.format('+' * min_temp)}{min_temp}C")

                    
class monthly_bonus_report:
    """
    This class takes the objects from list and draw single line chart on console
    """
    

    def getting_monthly_objects(self,record,year,month):
        calculating_records = []
        for index in range(len(record)):
            for key in record[index]:        
                if(record[index][key].startswith(year + '-' + month)):
                    calculating_records.append(record[index])

        return calculating_records
    
    def bonus_chart(self,req_objects):
        COLOR_BLUE = '\033[1;34;48m'
        COLOR_RED = '\033[1;31;48m'
        
        max_temperature = [ sub['Max TemperatureC'] for sub in req_objects]
        max_temp_convert_list = list(map(int, max_temperature))
        min_temperature = [ sub['Min TemperatureC'] for sub in req_objects]
        min_temp_convert_list = list(map(int, min_temperature))
        pkt = [ sub['PKT'] for sub in req_objects] or [ sub['PKST'] for sub in req_objects]

        for pkt,max_temp,min_temp in zip(pkt,max_temp_convert_list,min_temp_convert_list):
            print(f"{pkt}{COLOR_RED.format('+' * max_temp)}"
            f"{COLOR_BLUE.format('+' * min_temp)}{max_temp}C-{min_temp}C")


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', type=lambda date: datetime.strptime(date, '%Y'))
    parser.add_argument('-a', type=lambda date: datetime.strptime(date, '%Y/%m'))
    parser.add_argument('-c', type=lambda date: datetime.strptime(date, '%Y/%m'))

    return  parser.parse_args()

def main():
    arguments = parse_arguments()
    
    string_argv = sys.argv
    if arguments.a:
        for i in string_argv:
            if(not((i.endswith("py")) 
                or (i.endswith("-a"))
                or (i.endswith("-e"))
                or (i.endswith("-c")))):
                values = i.split("/")
                if(len(values) > 1):
                    year = values[0]
                    month = values[1]

                    record = Record_File()
                    record.read_file()

                    results = monthly_computing_results()
                    get_objects = results.getting_monthly_objects(record.weather_records,year,month)
                    
                    results.getmaximumaverage(get_objects)
                    results.getminimumaverage(get_objects)
                    results.gethumidityaverage(get_objects)
    if arguments.e:
        for i in string_argv:
            if(not((i.endswith("py"))
                or (i.endswith("-e"))
                or (i.endswith("-a"))
                or (i.endswith("-c")) )):
                values = i.split("/")
                if(len(values) <= 1):
                    years = values[0]

                    record = Record_File()
                    record.read_file()

                    results = yearly_computing_results()
                    get_objects = results.getting_yearly_objects(record.weather_records,years)

                    results.gethighesttemperature(get_objects)
                    results.getlowesttemperature(get_objects)
                    results.gethighesthumidity(get_objects)
    if arguments.c:
        for i in string_argv:
            if(not((i.endswith("py"))
                or (i.endswith("-c"))
                or (i.endswith("-a"))
                or (i.endswith("-e")))):
                values = i.split("/")
                if(len(values) > 1):
                    year = values[0]
                    month = values[1]

                    record = Record_File()
                    record.read_file()
                    
                    print("Press 1 for Multi line chart:")
                    print("Press 2 for Single line chart:")
                    option = input("Please Enter Option No:")
                    if(option == '1'):
                        monthly_report_chart = monthly_report()
                        getting_objects = monthly_report_chart.getting_monthly_objects(record.weather_records,year,month)

                        monthly_report_chart.monthly_chart(getting_objects)
                    elif(option == '2'):
                        bonus_report = monthly_bonus_report()
                        report = bonus_report.getting_monthly_objects(record.weather_records,year,month)
                        bonus_report.bonus_chart(report)
                    else:
                        print("Please Enter Valid Inputs!!!")
    
   
if __name__ == '__main__':
    main()
