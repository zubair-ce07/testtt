import csv
import calendar
import collections
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
        readings = collections.defaultdict(list)

        # Iterate for a year or a month
        months.append(calendar.month_abbr if self.operation == 'e' else calendar.month_abbr[int(report[1])])
        for month in months:
            self.filename[3] = month
            self.path = path + "".join(self.filename)
            if Path(self.path).is_file():
                with open(self.path) as csv_file:
                    lines = csv_file.read().splitlines()  # Get iterable lines
                    for entry in lines[2:-1]:
                        readings[month].append(entry.split(','))



