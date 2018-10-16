from datetime import datetime


class WeatherRecord:

    def __init__(self, record):
        self.max_temp = int(record.get('Max TemperatureC'))
        self.min_temp = int(record.get('Min TemperatureC'))
        self.mean_humidity = int(record[' Mean Humidity'])
        raw_date = record.get('PKT') or record.get('PKST')
        self.date = datetime.strptime(raw_date, '%Y-%m-%d')
