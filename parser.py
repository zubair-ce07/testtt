import calendar
import os
import csv

from dateutil.parser import parse

from weather import Weather


class WeatherParser:
    def __init__(self, directory_path, year, month):
        file_name = 'lahore_weather_{}_{}.txt'.format(
            year, calendar.month_abbr[month])

        file_path = os.path.join(directory_path, file_name)

        self._file = open(file_path)
        next(self._file)
        self._reader = csv.DictReader(self._file)

    def __enter__(self):
        return self

    def __iter__(self):
        for row in self._reader:
            try:
                date = parse(row.get('PKT'))
            except ValueError:
                continue

            try:
                value = Weather(
                    date,
                    int(row['Min TemperatureC']),
                    int(row['Max TemperatureC']),
                    int(row['Min TemperatureC']),
                    int(row[' Min Humidity']),
                    int(row['Max Humidity']),
                    int(row[' Mean Humidity'])
                )
            except ValueError:
                value = None

            yield value

    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, '_file') and not self._file.closed:
            self._file.close()
