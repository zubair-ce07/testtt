import calendar
import sys
import glob
import csv
import os

class DayReading:
    def __init__(self, date, max_temp, mean_temp, min_temp, max_humidity, mean_humidity):
        self.date = date
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity

class MonthReading:
    def __init__(self, path):
        if not os.path.exists(path):
            self.check = -1
            return
        self.check = 0
        self.days = []
        with open(path, 'r') as file_to_read:
            reader = csv.DictReader(file_to_read)
            for row in reader:
                day = DayReading(
                row['PKT'], 
                row['Max TemperatureC'],
                row['Mean TemperatureC'], 
                row['Min TemperatureC'],
                row['Max Humidity'], 
                row[' Mean Humidity']
                )
                self.days.append(day)
            self.month_name = f"{path[-7]}{path[-6]}{path[-5]}"
            self.year = f"{path[-12]}{path[-11]}{path[-10]}{path[-9]}"
            
class YearReading:
    def __init__(self, dir_path, year):
        if not os.path.exists(dir_path):
            self.check = -1
            return
        self.check = 0
        self.year = int(year)
        filenames = glob.glob(f"{dir_path}/Murree_weather_{year}_*.txt")
        self.days = []
        for filename in filenames:
            self.days.extend(MonthReading(filename).days)

class YearResults:
    def __init__(self, max_temp, max_temp_date, min_temp, min_temp_date, 
                 max_humidity, max_humidity_date, year):
        self.max_temp = max_temp
        self.max_temp_date = max_temp_date
        self.min_temp = min_temp
        self.min_temp_date = min_temp_date
        self.max_humidity = max_humidity
        self.max_humidity_date = max_humidity_date
        self.year = year
    
class MonthResults:
    def __init__(self, avg_high_temp, avg_low_temp, avg_mean_humidity, month, year):
        self.avg_high_temp = avg_high_temp
        self.avg_low_temp = avg_low_temp
        self.avg_mean_humidity = avg_mean_humidity
        self.month = month
        self.year = year

class ChartResults:
    def __init__(self, results, month, year):
        self.results = results
        self.month = month
        self.year = year
