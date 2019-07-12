import os
from record import Record
import csv
import calendar


class FileReader:
    def __init__(self, file_path, year, month=None):

        try:
            file_names = os.listdir(file_path)
        except:
            raise FileNotFoundError('Directory Not Found')
        years = []
        self.records = []
        try:
            type(int(year))
        except:
            raise ValueError('Format: YYYY')
        if month:
            try:
                month = int(month)
            except:
                raise ValueError('Format: MM')
            if month in range(1, len(calendar.month_name)):
                month = calendar.month_abbr[month]
            else:
                raise ValueError('Invalid Number')
        for file_name in file_names:
            if year in file_name:
                if month:
                    if month in file_name:
                        years.append(file_name)
                else:
                    years.append(file_name)
        if not years:
            raise ValueError('Not Available')
        for file_name in years:
            with open(file_path + os.path.sep + file_name) as csvfile:
                filereader = csv.DictReader(csvfile)
                for row in filereader:
                    new_record = Record(
                        row['PKT'], row['Max TemperatureC'],
                        row['Min TemperatureC'], row['Max Humidity'], row[' Mean Humidity'])
                    self.records.append(new_record)