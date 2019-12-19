from datetime import datetime


class WeatherRecord:

    def __init__(self, weather_record):
        self.record_date = datetime.strptime(weather_record['PKT'], '%Y-%m-%d')
        self.max_temperature = float(weather_record['Max TemperatureC'])
        self.mean_temperature = float(weather_record['Mean TemperatureC'])
        self.min_temperature = float(weather_record['Min TemperatureC'])
        self.max_humidity = float(weather_record['Max Humidity'])
        self.mean_humidity = float(weather_record['Mean Humidity'])
        self.min_humidity = float(weather_record['Min Humidity'])
