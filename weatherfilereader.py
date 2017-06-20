import os
import fnmatch
import calendar
import csv


class WeatherFilesReader(object):

    retrieved_records = None

    def __init__(self, directory=None):
        self.dir = directory
        self.retrieved_records = {}

    def set_directory(self, directory):
        self.dir = directory

    def get_filenames_by_month(self, year, month):
        return fnmatch.filter(os.listdir(self.dir), '*' + year + '_' + calendar.month_abbr[int(month)] + '.txt')

    def update_retrieved_records(self, new_records):
        self.retrieved_records.update(new_records)

    def read_by_month(self, year, month):
        records = {}
        if not any(key.startswith(year) and '-' + month + '-' in key
                   for key in self.retrieved_records):
            weather_filenames = self.get_filenames_by_month(year, month)
            for weather_file in weather_filenames:
                with open(os.path.join(self.dir, weather_file)) as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row['Max TemperatureC'] or row['Min TemperatureC'] or row['Max Humidity']:
                            records[row['PKT']] = {'max_temp': row['Max TemperatureC'],
                                                   'min_temp': row['Min TemperatureC'],
                                                   'max_humid': row['Max Humidity']}
            self.update_retrieved_records(records)
        else:
            records = {key: value for key, value in self.retrieved_records.iteritems()
                       if key.startswith(year) and '-' + month + '-' in key}

        return records

    def read_by_year(self, year):
        record = {}
        for month in range(1, 13):
            record.update(self.read_by_month(year, str(month)))
        return record

    def read_by_years(self, years):
        records = {}
        for year in years:
            records.update(self.read_by_year(year))
        return records
