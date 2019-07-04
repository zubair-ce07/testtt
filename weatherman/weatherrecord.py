from datetime import datetime


class WeatherRecord:
    def __init__(self, pkt, max_temp, min_temp, max_humidity, mean_humidity):
        self.pkt = pkt
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity

    @staticmethod
    def _verify_row(row):
        return all([row.get('PKT', row.get('PKST')), row.get('Max TemperatureC'), row.get('Min TemperatureC'),
                    row.get('Max Humidity'), row.get(' Mean Humidity')])

    @classmethod
    def from_map(cls, row):
        if cls._verify_row(row=row):
            return cls(pkt=datetime.strptime(row.get('PKT', row.get('PKST')), '%Y-%m-%d'),
                       max_temp=int(row['Max TemperatureC']),
                       min_temp=int(row['Min TemperatureC']),
                       max_humidity=int(row['Max Humidity']),
                       mean_humidity=int(row[' Mean Humidity']))
        return False
