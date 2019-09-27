import calendar
import csv
import datetime
import glob

from temperatureResults import TempReading


class FilesParser:

    def populate_temperatures(self, path, year):
        if len(year.split('/')) > 1:
            path = path + "/Murree_weather_" + year.split('/')[0] + "_" + calendar.month_abbr[int(year.split('/')[1])]
        else:
            path = path + "/Murree_weather_" + year
        temp_readings = []
        for temp_file_of_month in glob.glob(path + "*"):
            temperature_file = open(temp_file_of_month)
            temperature_file_reader = csv.DictReader(temperature_file)
            for day in temperature_file_reader:
                reading = TempReading(datetime.datetime.strptime(day.get('PKT', day.get('PKST')), '%Y-%m-%d'),
                                      day['Max TemperatureC'], day['Min TemperatureC'], day['Max Humidity'],
                                      day[' Mean Humidity'])
                temp_readings.append(reading)
        return temp_readings
