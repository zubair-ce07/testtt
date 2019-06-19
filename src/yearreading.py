import glob
from monthreading import MonthReading

class YearReading:
    def __init__(self, dir_path, year):
        self.year = int(year)
        self.full_path = dir_path + "/Murree_weather_" + year + "_*.txt"
        filenames = glob.glob(self.full_path)
        self.months = []
        for i in range(len(filenames)):
            month = MonthReading(filenames[i])
            self.months.append(month)

        
