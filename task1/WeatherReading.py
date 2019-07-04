

class WeatherReading:

    def __init__(self, weather_reading):
        self.pkt = weather_reading['PKT']
        max_temperature = weather_reading.get("Max TemperatureC")
        min_temperature = weather_reading.get("Min TemperatureC")
        mean_temperature = weather_reading.get("Mean TemperatureC")
        max_humidity = weather_reading.get("Max Humidity")
        min_humidity = weather_reading.get(" Min Humidity")
        mean_humidity = weather_reading.get(" Mean Humidity")
        if max_temperature:
            self.max_temperature = int(max_temperature)
        else:
            self.max_temperature = None

        if min_temperature:
            self.min_temperature = int(min_temperature)
        else:
            self.min_temperature = None

        if mean_temperature:
            self.mean_temperature = int(mean_temperature)
        else:
            self.mean_temperature = None

        if min_humidity:
            self.min_humidity = int(min_humidity)
        else:
            self.min_humidity = None

        if max_humidity:
            self.max_humidity = int(max_humidity)
        else:
            self.max_humidity = None

        if mean_humidity:
            self.mean_humidity = int(mean_humidity)
        else:
            self.mean_humidity = None
