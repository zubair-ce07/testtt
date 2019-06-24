import os
import WeatherReadings
import csv
import calendar


class WeatherDataExtractor:

    def __init__(self,month, year):
        self.allDataObjects = []
        self.month = month
        self.year = year

    def read_all_files(self):
        month = calendar.month_name(self.month)
        for i in os.listdir("weatherfiles"):
            try:
                csv_file = csv.DictReader(open("weatherfiles/%s" % i[:-11]+self.year+"_"+month[:4]+".txt"))
                for row in csv_file:
                    if row['PKT']:
                        reading = WeatherReadings.WeatherReadings(row)
                        self.allDataObjects.append(reading)
            except:
                continue
        print("all data:  ", self.allDataObjects[0].maxTemperature)
