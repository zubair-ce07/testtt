from datetime import datetime


class WeatherData:

    def __init__(self, row):
        self.max_temp = int(row.get('Max TemperatureC'))
        self.min_temp = int(row.get('Min TemperatureC'))
        self.mean_humidity = int(row[' Mean Humidity'])
        raw_date = row.get('PKT') or row.get('PKST')
        self.date = datetime.strptime(raw_date, '%Y-%m-%d')
