import glob
import datetime
import csv


class WeatherReadings:
    def __init__(self):
        self.weather_records = {}

    def insert_month_records(self, month_data):
        date = month_data[0].get('pkt')

        year_records = self.weather_records.get(date.year, {})
        year_records.update({date.month: month_data})
        self.weather_records.update({date.year: year_records})

    def extract_year_records(self, date):
        year_records = self.weather_records.get(date.year, {})
        return [day_record for month_records in year_records.values() for day_record in month_records]

    def extract_month_records(self, date):
        year_records = self.weather_records.get(date.year)
        return year_records.get(date.month) if year_records else None

    def read_weather_records(self, path_to_files):
        for file_path in glob.glob(f"{path_to_files}/*_weather_*_*.txt"):
            with open(file_path, 'r') as weather_record_file:
                records = csv.DictReader(weather_record_file)
                month_data = [self.convert_record(
                    record) for record in records if self.verify_record(record)]

            self.insert_month_records(month_data)

    def convert_record(self, record):
        date_value = record.get('PKT') or record.get('PKST')
        return {
            'max_temp': int(record.get('Max TemperatureC')),
            'min_temp': int(record.get('Min TemperatureC')),
            'max_humidity': int(record.get('Max Humidity')),
            'mean_humidity': int(record.get(' Mean Humidity')),
            'pkt': datetime.datetime.strptime(date_value, '%Y-%m-%d'),
        }

    def verify_record(self, record):
        date_value = record.get('PKT') or record.get('PKST')
        if record.get('Max TemperatureC') and\
                record.get('Min TemperatureC') and\
                record.get(' Mean Humidity') and\
                record.get('Max Humidity') and\
                date_value:
            return True
