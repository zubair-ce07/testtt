import math


class WeatherCalculator:

    def mean(self, weather_readings, feature):
        values = [reading[feature]
                  for reading in weather_readings if reading[feature] != -math.inf and reading[feature] != math.inf]
        total = sum(values)
        count = len(values)
        return (total / count)

    def date(self, reading):
        if 'PKT' in reading.keys():
            return reading['PKT']
        else:
            return reading['PKST']

    def calculate_weather(self, weather_readings):
        """This function calculates weather details."""

        stats = {}
        max_temp_reading = max(weather_readings, key=lambda wr: wr['Max TemperatureC'])
        min_temp_reading = min(weather_readings, key=lambda wr: wr['Min TemperatureC'])
        max_humidity_reading = max(weather_readings, key=lambda wr: wr['Max Humidity'])

        stats['Max Temperature'] = max_temp_reading['Max TemperatureC']
        stats['Max Temp Day'] = self.date(max_temp_reading)
        stats['Min Temperature'] = min_temp_reading['Min TemperatureC']
        stats['Min Temp Day'] = self.date(min_temp_reading)
        stats['Max Humidity'] = max_humidity_reading['Max Humidity']
        stats['Max Humidity Day'] = self.date(max_humidity_reading)
        stats['Avg Max Temp'] = self.mean(weather_readings, 'Max TemperatureC')
        stats['Avg Min Temp'] = self.mean(weather_readings, 'Min TemperatureC')
        stats['Avg Mean Humidity'] = self.mean(weather_readings, ' Mean Humidity')

        return stats
