from datetime import datetime


class WeatherReading:

    def __init__(self, readings):
        if readings["Max TemperatureC"] and readings["Min TemperatureC"] \
                and readings["Max Humidity"] and readings[" Mean Humidity"]:
            self.date = datetime.strptime(readings.get('PKT') or readings.get('PKST'), "%Y-%m-%d")
            self.max_temp = int(readings['Max TemperatureC'])
            self.min_temp = int(readings['Min TemperatureC'])
            self.max_humidity = int(readings['Max Humidity'])
            self.mean_humidity = int(readings[' Mean Humidity'])
