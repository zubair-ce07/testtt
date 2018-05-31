import os
from itertools import islice

_months_dictionary={1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",
                    8:"Aug",9:"Sept",10:"Oct",11:"Nov",12:"Dec"}
class WeatherReadingsPopulator:

    def __init__(self):
        self.weather_readings=[]
        self.files=[]

    def list_files(self, path: "files directory",
                   report_type: "required to populate relevant days data",
                   year, month: 'optional' = None):
        names_of_all_files=os.listdir(path)
        for file in names_of_all_files:
            if report_type == "-e":
                if file.find(str(year)) is not -1:
                    self.files.append(file)
            elif report_type in ["-a","-c"]:
                if file.find(year) is not -1 \
                        and file.find(_months_dictionary[month]) is not -1:
                    self.files.append(file)
                    break

    def populate_weather_readings(self,path):
        for file in self.files:
            f=open(path+"/"+file)
            for line in islice(f,1,None):
                weather_reading_from_line=line.split(",")
                weather_reading=[weather_reading_from_line[0],
                                 [weather_reading_from_line[1],
                                  weather_reading_from_line[2],
                                  weather_reading_from_line[3]],
                                 [weather_reading_from_line[7],
                                  weather_reading_from_line[8],
                                  weather_reading_from_line[9]]]
                self.weather_readings.append(weather_reading)




