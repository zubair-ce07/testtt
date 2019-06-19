import calendar
import sys

from dayreading import DayReading

class MonthReading:
    def __init__(self, path_to_file):
        self.days = []
        self.filepath = path_to_file
        try:
            self.file_to_read = open(self.filepath)
        except FileNotFoundError:
            print("Data for this month does not exist")
            sys.exit()
        
        self.file_to_read.readline()
        rows = self.file_to_read.readlines()
        for i in range(len(rows)):
            day_data = rows[i].split(',')
            day = DayReading(day_data[0], day_data[1], day_data[2], day_data[3], day_data[7], day_data[8])
            self.days.append(day)
        self.month_name = path_to_file[len(path_to_file)-7] + path_to_file[len(path_to_file)-6] + path_to_file[len(path_to_file)-5]
        self.month_num = list(calendar.month_abbr).index(self.month_name)
    