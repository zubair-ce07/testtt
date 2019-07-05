import csv
import glob
from WeatherReading import WeatherReading


class WeatherDataExtractor:

    def __init__(self, year, month="*"):
        self.month = month
        self.year = year
        self.weather_readings = []
        for name in glob.glob(f"weatherfiles/Murree_weather_{year}_{month}.txt"):
            for row in csv.DictReader(open(name)):
                reading = WeatherReading(row)
                self.weather_readings.append(reading)
