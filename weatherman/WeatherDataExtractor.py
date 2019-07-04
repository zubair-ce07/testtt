import csv
import glob
from WeatherReading import WeatherReading


class WeatherDataExtractor:
    weather_readings = []

    def __init__(self, year, month="*"):
        self.month = month
        self.year = year
        for name in glob.glob("weatherfiles/Murree_weather_%s_%s.txt" % (year, month)):
            for row in csv.DictReader(open(name)):
                reading = WeatherReading(row)
                self.weather_readings.append(reading)
