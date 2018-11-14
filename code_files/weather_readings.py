import glob
import datetime
import csv

from constants import REQUIRED_ATTRIBUTES


class WeatherReadings:
    def __init__(self):
        self.weather_records = {}

    def insert_month_records(self, month_record):
        date = month_record[0].get('pkt')

        year_records = self.weather_records.get(date.year, {})
        year_records.update({date.month: month_record})
        self.weather_records.update({date.year: year_records})

    def extract_year_records(self, date):
        year_records = self.weather_records.get(date.year, {})
        return sum(year_records.values(), [])

    def extract_month_records(self, date):
        return self.weather_records.get(date.year, {}).get(date.month)

    def read_weather_records(self, path_to_files):
        for file_path in glob.glob(f"{path_to_files}/*_weather_*_*.txt"):
            with open(file_path, 'r') as weather_record_file:
                records = csv.DictReader(weather_record_file)
                month_record = [self.convert_record(record) for record in records if self.is_valid(record)]

            self.insert_month_records(month_record)

    def convert_record(self, record):
        date_value = record.get('PKT') or record.get('PKST')
        return {
            'max_temp': int(record.get('Max TemperatureC')),
            'min_temp': int(record.get('Min TemperatureC')),
            'max_humidity': int(record.get('Max Humidity')),
            'mean_humidity': int(record.get(' Mean Humidity')),
            'pkt': datetime.datetime.strptime(date_value, '%Y-%m-%d'),
        }

    def is_valid(self, record):
        date_value = record.get('PKT') or record.get('PKST')
        return all([record.get(attr) for attr in REQUIRED_ATTRIBUTES] + [date_value])
