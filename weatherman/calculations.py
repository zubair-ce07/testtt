import math


class WeatherCalculator:
    def __init__(self, weather_readings):
        self.weather_readings = weather_readings

    def _mean(self, feature):
        values = [wr[feature] for wr in self.weather_readings if wr[feature] is not None]
        return (sum(values) / len(values))
    
    def _min(self, feature):
        reading = min(self.weather_readings, key=lambda wr: wr[feature] if wr[feature] is not None else math.inf)
        return (reading[feature], reading.get('PKT', reading.get('PKST')))

    def _max(self, feature):
        reading = max(self.weather_readings, key=lambda wr: wr[feature] if wr[feature] is not None else -math.inf)
        return (reading[feature], reading.get('PKT', reading.get('PKST')))

    def calculate_weather(self):
        stats = {}
        stats['Max Temperature'], stats['Max Temp Day'] = self._max('Max TemperatureC')
        stats['Min Temperature'], stats['Min Temp Day'] = self._min('Min TemperatureC')
        stats['Max Humidity'], stats['Max Humidity Day'] = self._max('Max Humidity')
        stats['Avg Max Temp'] = self._mean('Max TemperatureC')
        stats['Avg Min Temp'] = self._mean('Min TemperatureC')
        stats['Avg Mean Humidity'] = self._mean(' Mean Humidity')
        return stats
