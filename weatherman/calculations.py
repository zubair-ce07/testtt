import math


class WeatherCalculator:
    def __init__(self, weather_records):
        self.weather_records = weather_records

    def _mean(self, feature):
        readings = [wr[feature] for wr in self.weather_records if wr[feature]]
        return ((sum(readings)) / len(readings) if len(readings) > 0 else None)

    def _min(self, feature):
        reading = min(self.weather_records, key=lambda wr: wr[feature] if wr[feature] else math.inf)
        return (reading[feature], reading.get('PKT', reading['PKST'])
                if reading[feature] is not math.inf else (None, None))

    def _max(self, feature):
        reading = max(self.weather_records, key=lambda wr: wr[feature] if wr[feature] else -math.inf)
        return (reading[feature], reading.get('PKT', reading['PKST'])
                if reading[feature] is not -math.inf else (None, None))

    def calculate_weather(self):
        stats = {}
        stats['Max Temperature'], stats['Max Temp Day'] = self._max('Max TemperatureC')
        stats['Min Temperature'], stats['Min Temp Day'] = self._min('Min TemperatureC')
        stats['Max Humidity'], stats['Max Humidity Day'] = self._max('Max Humidity')
        stats['Avg Max Temp'] = self._mean('Max TemperatureC')
        stats['Avg Min Temp'] = self._mean('Min TemperatureC')
        stats['Avg Mean Humidity'] = self._mean(' Mean Humidity')
        return stats
