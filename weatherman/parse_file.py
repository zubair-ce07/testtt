import calendar
import collections
from pathlib import Path
from datetime import datetime


class ParseFile():
    """
    class for parsing the files and populating the readings data structure with correct data types"""
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
        if self.operation == '-e':
            months = calendar.month_abbr[1:]
        else:
            months.append(calendar.month_abbr[int(report[1])])
        for month in months:
            self.filename[3] = month
            self.path = path + "".join(self.filename)
            if Path(self.path).is_file():
                with open(self.path) as csv_file:
                    lines = csv_file.read().splitlines()  # Get iterable lines
                    for entry in lines[2:-1]:
                        day_entry = entry.split(',')
                        self.__convertDataType(day_entry)
                        readings[month].append(day_entry)
        return dict(readings)

    def __convertDataType(self, entry):
        entry[0] = datetime.strptime(entry[0], '%Y-%m-%d')
        for index in range(1, 21):
            entry[index] = float(entry[index]) if entry[index] else None
        entry[21] = str(entry[21])
        entry[22] = float(entry[22]) if entry[22] else None




