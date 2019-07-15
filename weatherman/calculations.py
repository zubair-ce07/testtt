import math


class WeatherCalculator:

    def maximum(self, weather_rows, feature):
        max_val = -math.inf
        day = -1
        for r in range(len(weather_rows[feature])):
            if weather_rows[feature][r] is not None:
                if int(weather_rows[feature][r]) > max_val:
                    max_val = int(weather_rows[feature][r])
                    day = weather_rows[0][r]
        return max_val, day

    def minimum(self, weather_rows, feature):
        min_val = math.inf
        day = -1
        for r in range(len(weather_rows[feature])):
            if weather_rows[feature][r] is not None:
                if int(weather_rows[feature][r]) < min_val:
                    min_val = int(weather_rows[feature][r])
                    day = weather_rows[0][r]
        return min_val, day

    def average(self, weather_rows, feature):
        total = 0
        count = 0
        for r in range(len(weather_rows[feature])):
            if weather_rows[feature][r] is not None:
                total += int(weather_rows[feature][r])
                count += 1
        if total > 0 and count > 0:
            return (total/count)
        else:
            return 0

    def calculate_weather(self, data):
        if len(data[0]) > 31:
            stats = {}
            stats['Max Temperature'], stats['Max Temp Day'] = self.maximum(data, 1)
            stats['Min Temperature'], stats['Min Temp Day'] = self.minimum(data, 2)
            stats['Max Humidity'], stats['Max Humidity Day'] = self.maximum(data, 3)
        else:
            stats = {}
            stats['Avg Max Temp'] = self.average(data, 1)
            stats['Avg Min Temp'] = self.average(data, 2)
            stats['Avg Mean Humidity'] = self.average(data, 4)
        return stats
