import csv
import glob

from weatherrecord import WeatherRecord


class WeatherParser:
    def __init__(self, path):
        self.path = path
        self._weather_records = self._parse_weather_records()

    def filtered_records(self, year=None, month=None):
        if month:
            return [r for r in self._weather_records if r.pkt.year == year and r.pkt.month == month]
        return [r for r in self._weather_records if r.pkt.year == year]

    def _parse_weather_records(self):
        file_names = glob.glob(f'{self.path}Murree_weather_*.txt')
        weather_records = []

        for file_name in file_names:
            with open(file_name, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                next(csv_reader)

                for row in csv_reader:
                    weather_record = WeatherRecord.is_valid_record(row)
                    if weather_record:
                        weather_records.append(weather_record)

        return weather_records
