import calendar
import sys
import glob
import csv

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
        self.days = []
        try:
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
                size = len(path)
                self.month_name = f"{path[size-7]}{path[size-6]}{path[size-5]}"
                self.year = f"{path[size-12]}{path[size-11]}{path[size-10]}{path[size-9]}"
                
        except FileNotFoundError:
            print("Data for this month does not exist")
            sys.exit()

class YearReading:
    def __init__(self, dir_path, year):
        self.year = int(year)
        filenames = glob.glob(f"{dir_path}/Murree_weather_{year}_*.txt")
        self.months = []
        for filename in filenames:
            month = MonthReading(filename)
            self.months.append(month)

class YearResults:
    def __init__(self, max_temp, max_temp_date, min_temp, min_temp_date, 
                 max_humidity, max_humidity_date):
        self.max_temp = max_temp
        self.max_temp_date = max_temp_date
        self.min_temp = min_temp
        self.min_temp_date = min_temp_date
        self.max_humidity = max_humidity
        self.max_humidity_date = max_humidity_date
    
class MonthResults:
    def __init__(self, avg_high_temp, avg_low_temp, avg_mean_humidity):
        self.avg_high_temp = avg_high_temp
        self.avg_low_temp = avg_low_temp
        self.avg_mean_humidity = avg_mean_humidity

class ChartResults:
    def __init__(self, high_temps, low_temps, high_dates, low_dates, month, year):
        self.high_temps = high_temps
        self.low_temps = low_temps
        self.high_dates = high_dates
        self.low_dates = low_dates
        self.month = month
        self.year = year
