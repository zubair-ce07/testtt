from datetime import datetime


class WeatherRecord:
    _weather_records = []

    def __init__(self, row):
        self.pkt = datetime.strptime(row.get('PKT', row.get('PKST')), '%Y-%m-%d')
        self.max_temp = int(row['Max TemperatureC'])
        self.min_temp = int(row['Min TemperatureC'])
        self.max_humidity = int(row['Max Humidity'])
        self.mean_humidity = int(row[' Mean Humidity'])

    @staticmethod
    def is_valid_record(row):
        if all([row.get('PKT', row.get('PKST')), row.get('Max TemperatureC'),
                row.get('Min TemperatureC'),row.get('Max Humidity'),
                row.get(' Mean Humidity')]):
            return WeatherRecord(row)
        return False
