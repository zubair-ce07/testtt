import os.path
import re
import csv
import datetime
from datetime import datetime
from records import Records


class ReadWeatherData:
    """This class reads parses the files and updates the records"""

    files = []

    def __init__(self, path):
        self.path = path

    def read_data(self):
        list_of_records = []
        for file in self.files:
            with open(self.path+file) as csv_file:
                reader = csv.DictReader(csv_file, restval='')
                for row in reader:
                    dates = row.get('PKT') or row.get('PKST')
                    date = datetime.strptime(dates, "%Y-%m-%d")
                    record = (Records(date,
                                      row['Max TemperatureC'],
                                      row['Mean TemperatureC'],
                                      row['Min TemperatureC'],
                                      row['Max Humidity'],
                                      row[' Mean Humidity'],
                                      row[' Min Humidity']))
                    list_of_records.append((record))

        return list_of_records

    def read_data_year(self, year):
        for f in os.listdir(self.path):
            if re.match('.*'+year+'.*', f):
                self.files.append(f)

    def read_data_file_month(self, year, month):
        for f in os.listdir(self.path):
            if re.match('.*'+year+'_'+month+'.*', f):
                self.files.append(f)
