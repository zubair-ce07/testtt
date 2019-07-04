import csv
import glob
from WeatherReading import WeatherReading


class WeatherDataExtractor:

    def __init__(self, year, month="*"):
        self.month = month
        self.year = year
        self.all_data_obj = []

    def read_all_files(self):
        for name in glob.glob("weatherfiles/Murree_weather_"+self.year+"_"+self.month+".txt"):
            for row in csv.DictReader(open(name)):
                reading = WeatherReading(row)
                self.all_data_obj.append(reading)
