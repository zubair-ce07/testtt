
class WeatherResultsCalculator:

    def calculate_yearly_high_low_weather(self, weather_readings):
        high = max(weather_readings, key=lambda x: x.high_temperature)
        low = min(weather_readings, key=lambda x: x.low_temperature)
        humidity = max(weather_readings, key=lambda x: x.humidity)
        return [high, low, humidity]

    def calculate_monthly_avg_weather(self, weather_readings):
        avg_high_temperature = sum([reading.high_temperature for reading in weather_readings]) / len(weather_readings)
        avg_low_temperature = sum([reading.low_temperature for reading in weather_readings]) / len(weather_readings)
        avg_mean_humidity = sum([reading.mean_humidity for reading in weather_readings]) / len(weather_readings)
        return [int(avg_high_temperature), int(avg_low_temperature), int(avg_mean_humidity)]
