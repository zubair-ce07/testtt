import csv
import glob
from datetime import datetime

from weatherrecord import WeatherRecord


class WeatherParser:

    def __init__(self, path):

        self.path = path

        self._weather_records = self._parse_weather_records()

    _PKT = 'PKT'
    _PKST = 'PKST'
    _MAX_TEMPERATURE = 'Max TemperatureC'
    _MIN_TEMPERATURE = 'Min TemperatureC'
    _MAX_HUMIDITY = 'Max Humidity'
    _MEAN_HUMIDITY = ' Mean Humidity'

    def _is_valid_row(self, weather_row):

        if 'PKT' in weather_row.keys():
            if not weather_row[self._PKT]:
                return False
        else:
            if not weather_row[self._PKST]:
                return False

        if not weather_row[self._MAX_TEMPERATURE]:
            return False

        if not weather_row[self._MIN_TEMPERATURE]:
            return False

        if not weather_row[self._MAX_HUMIDITY]:
            return False

        if not weather_row[self._MEAN_HUMIDITY]:
            return False

        return True

    def of(self, year=None, month=None):
        if month:
            return [x for x in self._weather_records if x.pkt.year == year
                    if month if month == x.pkt.month]
        else:
            return [x for x in self._weather_records if x.pkt.year == year]

    def _parse_weather_records(self):

        file_paths = glob.glob(f'{self.path}Murree_weather_*.txt')
        weather_records = []

        for file_path in file_paths:

            with open(file_path, mode='r') as csv_file:

                csv_reader = csv.DictReader(csv_file, delimiter=',')
                next(csv_reader)

                for row in csv_reader:
                    if not self._is_valid_row(row):
                        continue

                    record_date = datetime.strptime(
                        row[self._PKT if row.get(self._PKT) else self._PKST],
                        '%Y-%m-%d').date()

                    weather_records.append(
                        WeatherRecord(
                            pkt=record_date,
                            max_temp=int(row[self._MAX_TEMPERATURE]),
                            min_temp=int(row[self._MIN_TEMPERATURE]),
                            max_humidity=int(row[self._MAX_HUMIDITY]),
                            mean_humidity=int(row[self._MEAN_HUMIDITY]),
                            month_name=record_date.strftime('%B')
                        )
                    )

        return weather_records
