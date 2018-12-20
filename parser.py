import glob
import csv
from datetime import datetime

from temperature import Weather
import colors


class DataParser:

    def read_weather_data(self, files_record):
        weather_data = []
        for file_name in files_record:
            try:
                with open(file_name, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for line in csv_reader:
                        formatted_date = datetime.strptime(list(line.values())[0], '%Y-%m-%d')

                        if self.fun(line):
                            max_temperature = line['Max TemperatureC']
                            mean_temperature = line['Mean TemperatureC']
                            min_temperature = line['Min TemperatureC']
                            max_humidity = line['Max Humidity']
                            mean_humidity = line[' Mean Humidity']
                            min_humidity = line[' Min Humidity']

                            weather = Weather(formatted_date, max_temperature, mean_temperature, min_temperature,
                                              max_humidity, mean_humidity, min_humidity)
                            weather_data.append(weather)
            except FileNotFoundError as err:
                    print(err)
        return weather_data

    def fun(self, line):
        validation_fields = ['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC', 'Max Humidity',
                             ' Mean Humidity', ' Min Humidity']
        return all([line[field] for field in validation_fields])

    def weather_record(self, year_date, directory_path, month_date=0):
        if month_date == 0:
            month_date = '*'
        else:
            month_date = datetime.strftime(datetime.strptime(repr(month_date), '%m'), '%b')
        files_record = glob.glob(f"{directory_path}*{repr(year_date)}?{month_date}.txt")
        try:
            if files_record:
                return files_record
            else:
                raise ValueError(f"{colors.RED}Record Not Found{colors.RESET}")
        except ValueError as ve:
            print(ve)
