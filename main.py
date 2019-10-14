import argparse
import os
import csv
import sys
from datetime import datetime

from calculate_result import monthly_computing_results
from calculate_result import yearly_computing_results

from report import monthly_report
from report import monthly_bonus_report


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

                
def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', type=lambda date: datetime.strptime(date, '%Y'))
    parser.add_argument('-a', type=lambda date: datetime.strptime(date, '%Y/%m'))
    parser.add_argument('-c', type=lambda date: datetime.strptime(date, '%Y/%m'))

    return  parser.parse_args()

def main():
    arguments = parse_arguments()
    
    record = Record_File()
    record.read_file()

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
                or (i.endswith("-c")))):
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

                    print("Press 1 for Monthly report in multi line")
                    print("Press 2 for Monthly report in single line")
                    option = input("Please Enter A Option: ")
                    if option == '1':
                        monthly_report_chart = monthly_report()
                        getting_objects = monthly_report_chart.getting_monthly_objects(record.weather_records,year,month)
                        monthly_report_chart.monthly_chart(getting_objects)
                    elif option == '2':
                        bonus_report = monthly_bonus_report()
                        report = bonus_report.getting_monthly_objects(record.weather_records,year,month)
                        bonus_report.bonus_chart(report)
                    else:
                        print("PLease Enter Valid Inputs!!!")
    
   
if __name__ == '__main__':
    main()
