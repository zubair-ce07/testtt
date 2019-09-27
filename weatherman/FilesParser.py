import calendar
import csv
import datetime
import os
from temperatureResults import TempResult


class FilesParser:

    def populate_yearly_temps(self, path, year):
        temp_readings = []
        for month in range(1, 13):
            temp_path = year + "/" + str(month)
            temp_readings += self.populate_monthly_temps(path, temp_path)
        return temp_readings

    def populate_monthly_temps(self, path, month):
        month_n = month.split('/')[1]
        temp_readings = []
        temp_path = path + "/Murree_weather_" + month.split('/')[0] + "_" + calendar.month_abbr[int(month_n)] + ".txt"
        if os.path.isfile(temp_path):
            temperature_file = open(temp_path)
            temperature_file_reader = csv.DictReader(temperature_file)
            for day in temperature_file_reader:
                reading = TempResult(datetime.datetime.strptime(day.get('PKT', day.get('PKST')), '%Y-%m-%d'),
                                     day['Max TemperatureC'], day['Min TemperatureC'], day['Max Humidity'],
                                     day[' Mean Humidity'])
                temp_readings.append(reading)
        return temp_readings
