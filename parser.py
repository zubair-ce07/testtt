import calendar
import os
import csv

from dateutil.parser import parse

from weather import Weather


class WeatherParser:
    def __init__(self, directory_path, year, month):
        file_name = 'lahore_weather_{}_{}.txt'.format(
            year, calendar.month_abbr[month])

        self.file_path = os.path.join(directory_path, file_name)

    def __iter__(self):
        with open(self.file_path) as weather_data:
            next(weather_data)
            weather_reader = csv.DictReader(weather_data)

            for row in weather_reader:
                try:
                    date = parse(row.get('PKT') or row.get('PKST'))
                except ValueError:
                    continue

                try:
                    value = Weather(
                        date,
                        int(row['Min TemperatureC']),
                        int(row['Max TemperatureC']),
                        int(row['Mean TemperatureC']),
                        int(row[' Min Humidity']),
                        int(row['Max Humidity']),
                        int(row[' Mean Humidity'])
                    )
                except ValueError:
                    value = None

                yield value
