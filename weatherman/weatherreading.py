from datetime import datetime


class WeatherReading:

    def __init__(self, readings):
        self.date = datetime.strptime(readings.get('PKT') or readings.get('PKST'), "%Y-%m-%d")
        self.max_temp = int(readings['Max TemperatureC']) if readings['Max TemperatureC'] else None
        self.min_temp = int(readings['Min TemperatureC']) if readings['Min TemperatureC'] else None
        self.max_humidity = int(readings['Max Humidity']) if readings['Max Humidity'] else None
        self.mean_humidity = int(readings[' Mean Humidity']) if readings[' Mean Humidity'] else None
