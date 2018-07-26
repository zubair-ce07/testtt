import os

import glob

import sys


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
            opened_file = open(txt_file)
            keys = str(opened_file.readline())  #Read headings
            keys = keys.split(',')
            for line in opened_file.readlines()[1:]:
                line = line.replace('\n', '')
                line_content_list = line.split(',')
                year_month_date = line_content_list[0].split('-')
                self.weather_data.append(self.populate_data(keys,line_content_list,year_month_date))
            opened_file.close()
        

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
    

    def yearly_temperature_and_humidity_calulator(self,weather_data, year):
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
                            first_iteration = False
                            self.calculated_results = {
                                                        "MaxYearlyTempreature": temp_data.get("Max TemperatureC")
                                                        ,"HighestTempretureDay": day
                                                        ,"HighestTempretureMonth": month_names[month]
                                                        ,"MinYearlyTempreature": temp_data.get("Min TemperatureC")
                                                        ,"LowestTempretureDay": day
                                                        ,"LowestTempretureMonth": month_names[month]
                                                        ,"Humidity": temp_data.get(" Mean Humidity")
                                                        ,"MostHumidDay": day
                                                        ,"MostHumidMonth": month_names[month]
                                                        }
                        elif ((not temp_data.get("Max TemperatureC") == "" or
                                not temp_data.get("Min TemperatureC") == "") and
                                not temp_data.get(" Mean Humidity") ==""):
                            if (float(temp_data.get("Max TemperatureC")) > 
                                    float(self.calculated_results.get("MaxYearlyTempreature"))):
                                self.calculated_results["MaxYearlyTempreature"] = temp_data.get("Max TemperatureC")
                                self.calculated_results["HighestTempretureMonth"] = month_names[month]
                                self.calculated_results["HighestTempretureDay"] = day
                            elif (float(temp_data.get("Min TemperatureC")) < 
                                    float(self.calculated_results.get("MinYearlyTempreature"))):
                                self.calculated_results["MinYearlyTempreature"] = temp_data.get("Min TemperatureC")
                                self.calculated_results["LowestTempretureMonth"] = month_names[month]
                                self.calculated_results["LowestTempretureDay"] = day
                            
                            if(float(temp_data.get(" Mean Humidity")) >
                                    float(self.calculated_results.get("Humidity"))):
                                self.calculated_results["Humidity"] = temp_data.get(" Mean Humidity")
                                self.calculated_results["MostHumidDay"]  = day
                                self.calculated_results["MostHumidMonth"] = month_names[month]
        print(self.calculated_results)

                            
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
        ResultsCalculatorInstance.yearly_temperature_and_humidity_calulator(
            WeatherRecordInstance.weather_data, str(sys.argv[3])
            )
    
