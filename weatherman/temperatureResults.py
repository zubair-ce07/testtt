from datetime import datetime


class DayReading:
    def __init__(self, day_weather_reading):
        self.date = datetime.strptime(day_weather_reading.get('PKT', day_weather_reading.get('PKST')), '%Y-%m-%d')
        self.high_temperature = int(day_weather_reading['Max TemperatureC'])
        self.low_temperature = int(day_weather_reading['Min TemperatureC'])
        self.humidity = int(day_weather_reading['Max Humidity'])
        self.mean_humidity = int(day_weather_reading[' Mean Humidity'])
