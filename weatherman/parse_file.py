import csv
import calendar
from pathlib import Path


class ParseFile():
    def __init__(self):
        self.filename = ["lahore_weather_", 'year', '_', 'month', '.txt']
        self.operation = None
        self.path = None

    def parse(self, operation, report, path):
        self.filename[1] = report[0]
        self.operation = operation
        months = []
        
        # Iterate for a year or a month
        months.append(calendar.month_abbr if self.operation == 'e' else calendar.month_abbr[2])
        for month in months:
            self.filename[3] = month
            self.path = path + "".join(self.filename)
            if Path(self.path).is_file():
                with open(self.path) as csv_file:
                    reader = csv.reader(csv_file)
                    for entry in reader:
                            print(entry)




