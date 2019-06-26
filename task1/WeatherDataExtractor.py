import csv
import glob
from WeatherReading import WeatherReading


class WeatherDataExtractor:

    def __init__(self):
        self.all_data_objects = []

    def read_all_files(self, year, month=0):
        if not month:
            for name in glob.glob("weatherfiles/Murree_weather_"+year+"_*.txt"):
                csv_file = csv.DictReader(open(name))
                for row in csv_file:
                    if row['PKT']:
                        reading = WeatherReading(row)
                        self.all_data_objects.append(reading)
        else:
            try:
                csv_file = csv.DictReader(open("weatherfiles/Murree_weather_"+year+"_"+month+".txt"))
            except ValueError:
                print("Data not available")
                return
            for row in csv_file:
                if 'PKT' in row:
                    reading = WeatherReading(row)
                    self.all_data_objects.append(reading)
        return self.all_data_objects
