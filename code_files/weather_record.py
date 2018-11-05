from datetime import datetime


class WeatherRecord:
    def __init__(self, record):
        day = record.get('PKT') or record.get('PKST')
        self.pkt = datetime.strptime(day, '%Y-%m-%d')
        self.max_temp = int(record['Max TemperatureC'])
        self.min_temp = int(record['Min TemperatureC'])
        self.max_humidity = int(record['Max Humidity'])
        self.mean_humidity = int(record[' Mean Humidity'])
