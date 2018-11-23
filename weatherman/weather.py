import os.path
import re
import csv
import datetime
from datetime import datetime
from records import Records


class ReadWeatherData:
    """This class reads parses the files and updates the records"""

    files = []
    list_of_records = []

    def __init__(self, path):
        self.path = path

    def read_data(self):
        for file in self.files:
            with open(self.path+file) as csv_file:
                reader = csv.DictReader(csv_file, restval='')
                for row in reader:
                    dates = row.get('PKT') or row.get('PKST')
                    date = datetime.strptime(dates, "%Y-%m-%d")
                    if row['Max TemperatureC'] != "":
                        max_temp = row['Max TemperatureC']
                    if row['Mean TemperatureC'] != "":
                        mean_tem = row['Mean TemperatureC']
                    if row['Min TemperatureC'] != "":
                        min_tem = row['Min TemperatureC']
                    if row['Max Humidity'] != "":
                        max_hum = row['Max Humidity']
                    if row[' Mean Humidity'] != "":
                        mean_hum = row[' Mean Humidity']
                    if row[' Min Humidity'] != "":
                        min_hum = row[' Min Humidity']
                    self.list_of_records.append(Records(date, max_temp, mean_tem,
                                                        min_tem, max_hum, mean_hum, min_hum))
        return self.list_of_records

    def read_data_year(self, year):
        """this function reads files of the specific year"""
        for f in os.listdir(self.path):
            if re.match('.*'+year+'.*', f):
                self.files.append(f)

    def read_data_file_month(self, year, month):
        """reads files for a specific months and store them in
            files list"""
        for f in os.listdir(self.path):
            if re.match('.*'+year+'_'+month+'.*', f):
                self.files.append(f)
