import calendar
import csv
from datetime import datetime
from glob import glob


class WeatherData:

    def __init__(self, max_temp=None, min_temp=None,
                 mean_humidity=None, date=None):
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.mean_humidity = mean_humidity
        if date is not None:
            self.date = datetime.strptime(date, '%Y-%m-%d')
        else:
            self.date = date

    def all_weather_record(self, dir_path):
        files_path = glob(dir_path + r'*' + '.txt')
        records_list = []
        for file_path in files_path:
            with open(file_path) as current_file:
                reader = csv.DictReader(current_file)
                for row in reader:
                    if '' or None in (row.get('Max TemperatureC'),
                                      row.get('Min TemperatureC'),
                                      row.get(' Mean Humidity'),
                                      row.get('PKT')):
                        continue
                    try:
                        record = WeatherData(
                            max_temp=int(row['Max TemperatureC']),
                            min_temp=int(row['Min TemperatureC']),
                            mean_humidity=int(row[' Mean Humidity']),
                            date=row['PKT'])
                    except ValueError:
                        pass
                    records_list.append(record)
        return records_list

    def month_record(self, data_list, month):
        req_date = datetime.strptime(month, "%Y/%m")

        return [day for day in data_list
                if (day.date.year == req_date.year) and
                (day.date.month == req_date.month)]

    def year_record(self, data_list, year):
        req_date = datetime.strptime(year, "%Y")

        return [day for day in data_list
                if (day.date.year == req_date.year)]
