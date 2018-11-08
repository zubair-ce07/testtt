#!/usr/bin/python3.6
import csv
import datetime

class ReadWeather:
    def __init__(self):
        self.file_data = {}

    def read_file(self, file_path):
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            for row in csv_reader:
                date_value = row.get('PKT') if row.get('PKT') else row.get('PKST')
                date_value = datetime.datetime.strptime(date_value, '%Y-%m-%d')
                max_humidity = int(row.get('Max Humidity')) if row.get('Max Humidity') else None
                mean_humidity = int(row.get(' Mean Humidity')) if row.get(' Mean Humidity') else None
                max_temperature = int(row.get('Max TemperatureC')) if row.get('Max TemperatureC') else None
                min_temperature = int(row.get('Min TemperatureC')) if row.get('Min TemperatureC') else None
                
                self.file_data.setdefault('pkt', []).append(date_value)
                self.file_data.setdefault('max_temperature', []).append(max_temperature)
                self.file_data.setdefault('min_temperature', []).append(min_temperature)
                self.file_data.setdefault('max_humidity', []).append(max_humidity)
                self.file_data.setdefault('mean_humidity', []).append(mean_humidity)
