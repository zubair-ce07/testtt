import glob
from datetime import datetime
import csv


class WeatherData:
    def __init__(self, row):
        if row.get('PKT'):
            self.date = datetime.strptime(row.get('PKT'), '%Y-%m-%d')
        else:
            self.date = datetime.strptime(row.get('PKST'), '%Y-%m-%d')
        self.max_temp = self.convert_val(row['Max TemperatureC'], int)
        self.min_temp = self.convert_val(row['Min TemperatureC'], int)
        self.mean_temp = self.convert_val(row['Mean TemperatureC'], int)
        self.max_humidity = self.convert_val(row['Max Humidity'], int)
        self.min_humidity = self.convert_val(row[' Min Humidity'], int)
        self.mean_humidity = self.convert_val(row[' Mean Humidity'], int)

    def convert_val(self, val, typ):
        if val == '':
            val = 0
        return typ(val)


class WeatherRecords:
    def __init__(self, path):
        self.files_data = []
        for file in glob.glob(f"{path}/Murree_weather_{'*'}_{'*'}.txt"):
            for row in csv.DictReader(open(file)):
                self.files_data.append(WeatherData(row))
