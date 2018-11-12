import glob
import datetime
import csv


class WeatherReadings:
    def __init__(self):
        self.weather_records = {}

    def add_month(self, month_data):
        date = month_data[0].get('pkt')

        if self.weather_records.get(date.year):
            self.weather_records[date.year][date.month] = month_data
        else:
            self.weather_records[date.year] = {date.month: month_data}

    def extract_year_readings(self, date):
        year_records = self.weather_records.get(date.year)
        if year_records:
            return [weather_record for month in year_records for weather_record in year_records[month]]
        return

    def extract_month_readings(self, date):
        year_records = self.weather_records.get(date.year)
        return year_records.get(date.month) if year_records else None

    def read_weather_records(self, path_to_files):
        files_path = glob.glob(f"{path_to_files}/*_weather_*_*.txt")

        for file_path in files_path:
            with open(file_path, 'r') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                month_data = []

                for row in csv_reader:
                    if not self.check_records_availability(row):
                        continue

                    month_data.append(self.convert_records(row))

            self.add_month(month_data)

    def convert_records(self, record):
        date_value = record.get('PKT') or record.get('PKST')
        return {
            'max_temp': int(record.get('Max TemperatureC')),
            'min_temp': int(record.get('Min TemperatureC')),
            'max_humidity': int(record.get('Max Humidity')),
            'mean_humidity': int(record.get(' Mean Humidity')),
            'pkt': datetime.datetime.strptime(date_value, '%Y-%m-%d'),
        }

    def check_records_availability(self, record):
        date_value = record.get('PKT') or record.get('PKST')
        if record.get('Max TemperatureC') and\
                record.get('Min TemperatureC') and\
                record.get(' Mean Humidity') and\
                record.get('Max Humidity') and\
                date_value:
            return True

        return
