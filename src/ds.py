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
    def __init__(self, path_to_file):
        self.days = []
        self.filepath = path_to_file
        try:
            self.file_to_read = open(self.filepath)
        except FileNotFoundError:
            print("Data for this month does not exist")
            sys.exit()
        reader = csv.DictReader(self.file_to_read)
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
        self.month_name = path_to_file[len(path_to_file)-7] + path_to_file[len(path_to_file)-6] + path_to_file[len(path_to_file)-5]
        self.month_num = list(calendar.month_abbr).index(self.month_name)
        self.year = path_to_file[len(path_to_file)-12] + path_to_file[len(path_to_file)-11] + path_to_file[len(path_to_file)-10] + path_to_file[len(path_to_file)-9]
        

class YearReading:
    def __init__(self, dir_path, year):
        self.year = int(year)
        self.full_path = dir_path + "/Murree_weather_" + year + "_*.txt"
        filenames = glob.glob(self.full_path)
        self.months = []
        for i in range(len(filenames)):
            month = MonthReading(filenames[i])
            self.months.append(month)

class YearResults:
    def __init__(self, max_temp, max_temp_date, min_temp, min_temp_date, max_humidity, max_humidity_date):
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
