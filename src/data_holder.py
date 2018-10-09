from datetime import datetime


class WeatherData:

    def __init__(self, row):
        self.max_temp = int(row.get('Max TemperatureC'))
        self.min_temp = int(row.get('Min TemperatureC'))
        self.mean_humidity = int(row[' Mean Humidity'])
        self.date = datetime.strptime(row.get('PKT') or row.get('PKST'), '%Y-%m-%d')
