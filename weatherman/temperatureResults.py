import datetime


class WeatherReading:
    def __init__(self, weather_readings):
        self.date = datetime.datetime.strptime(weather_readings.get('PKT', weather_readings.get('PKST')), '%Y-%m-%d')
        self.high_temperature = int(weather_readings['Max TemperatureC'])
        self.low_temperature = int(weather_readings['Min TemperatureC'])
        self.humidity = int(weather_readings['Max Humidity'])
        self.mean_humidity = int(weather_readings[' Mean Humidity'])
