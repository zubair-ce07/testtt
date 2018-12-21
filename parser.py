import glob
import csv
from datetime import datetime

from temperature import Weather
import color


class DataParser:

    def read_weather_data(self, files_record):
        weather_data = []
        for file_name in files_record:
            try:
                with open(file_name, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for record in csv_reader:
                        if 'PKT' in record.keys():
                            formatted_date = datetime.strptime(record['PKT'], '%Y-%m-%d')
                        else:
                            formatted_date = datetime.strptime(record['PKST'], '%Y-%m-%d')
                        if self.validate_record(record):
                            max_temperature = record['Max TemperatureC']
                            mean_temperature = record['Mean TemperatureC']
                            min_temperature = record['Min TemperatureC']
                            max_humidity = record['Max Humidity']
                            mean_humidity = record[' Mean Humidity']
                            min_humidity = record[' Min Humidity']

                            weather = Weather(formatted_date, max_temperature, mean_temperature, min_temperature,
                                              max_humidity, mean_humidity, min_humidity)
                            weather_data.append(weather)
            except FileNotFoundError as err:
                    print(err)
        return weather_data

    def validate_record(self, record):
        validation_fields = ['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC',
                             'Max Humidity', ' Mean Humidity', ' Min Humidity']
        return all([record[field] for field in validation_fields])

    def find_record(self, year_date, directory_path, month_date=0):
        if month_date == 0:
            month_date = '*'
        else:
            month_date = datetime.strftime(datetime.strptime(repr(month_date), '%m'), '%b')
        files_record = glob.glob(f"{directory_path}*{repr(year_date)}?{month_date}.txt")
        try:
            if files_record:
                return files_record
            else:
                raise ValueError(f"{color.RED}Record Not Found{color.RESET}")
        except ValueError as ve:
            print(ve)
