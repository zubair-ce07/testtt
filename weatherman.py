import os

import glob

import sys


VALID_OPTIONS = [
                    '-e','-c', '-a'
                 ]

USAGE_STRING = "Python weatherman.py [Path to weatherman files]"\
                " [Valid Options] [Valid Month, Year]"


class WeatherRecord:
    def __init__(self):
        self.weather_data = None
        self.month_names = {
                            "1":"Jan", "2":"Feb",
                            "3":"Mar", "4":"Apr",
                            "5":"May", "6":"Jun",
                            "7":"Jul", "8":"Aug",
                            "9":"Sep", "10":"Oct",
                            "11":"Nov", "12":"Dec"
                            }


    def read_data_from_files(self,folder_path):
        txt_files = glob.glob(folder_path+"/*.txt")  #Read text files
        self.weather_data = []
        for txt_file in txt_files:
            opened_file = open(txt_file)
            keys = str(opened_file.readline())  #Read headings
            keys = keys.split(',')
            for line in opened_file.readlines()[1:]:
                line = line.replace('\n', '')
                line_content_list = line.split(',')
                year_month_date = line_content_list[0].split('-')
                self.weather_data.append(self.populate_data(keys,line_content_list,year_month_date))
            opened_file.close()
        # for data in self.weather_data:
        #     x  = data.get("2008",{}).get('1',{}).get("31",{}).get("MeanDew PointC")
        #     if x is not None:
        #         print x



    def populate_data(self,keys,line_content_list,year_month_date):
        temp_dictionary = {}
        sub_key_level_dictionary = {}
        for key, weather_data in zip(keys, line_content_list):
            key = key.replace('\n','')
            temp_dictionary[key] = weather_data
            sub_key_level_dictionary = {
                                        str(year_month_date[0]):{
                                            str(year_month_date[1]):{
                                                str(year_month_date[2]):
                                                    temp_dictionary
                                                }
                                            }
                                        }
        return sub_key_level_dictionary
    

class ResultsCalculator:
    def __init__(self):
        self.calculated_results = None

    
    def calculate_average(self):

        pass
    

    def calculate_yearly_min_max_tempreture(self,weather_data, year):
        self.calculated_results = {}
        first_iteration = True
        for data in weather_data:
            month_level_data = data.get(year)
            if month_level_data is not None:
                for month in month_level_data:
                    day_level_data = month_level_data.get(month)
                    for day in day_level_data:
                        temp_data  = day_level_data.get(day)
                        if first_iteration:
                            self.calculated_results = {
                                                        "MaxYearlyTempreature":temp_data.get("Max TemperatureC")
                                                        ,"MinYearlyTempreature":temp_data.get("Min TemperatureC")
                                                        }
                        else:
                            if temp_data.get("Max TemperatureC") > self.calculated_results.get("MaxYearlyTempreature"):
                                self.calculated_results["MaxYearlyTempreature"] = temp_data.get("Max TemperatureC")

                            if temp_data.get("Min Temperature") > self.calculated_results.get("MinYearlyTempreature"):
                                self.calculated_results["MinYearlyTempreature"] = temp_data.get("Min Temperature")

        print(self.calculated_results.get("MaxYearlyTempreature"))
        print(self.calculated_results.get("MinYearlyTempreature"))

                            

def usage_printer():
    print("Usage:")
    print(USAGE_STRING)
    print("Options:")
    print(VALID_OPTIONS)
    sys.exit()


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

    if sys.argv[2] == '-a':
        pass
    elif sys.argv[2] == '-c':
        pass
    elif sys.argv[2] == '-e':
        ResultsCalculatorInstance.calculate_yearly_min_max_tempreture(
            WeatherRecordInstance.weather_data, str(sys.argv[3])
            )
    
