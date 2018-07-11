class WeatherReading:

    def __init__(self, readings):
        self.pkt = readings.get('PKT', readings.get('PKST'))
        self.max_temperature = (int(readings.get('Max TemperatureC'))
                                if readings.get('Max TemperatureC') else None)
        self.min_temperature = (int(readings.get('Min TemperatureC'))
                                if readings.get('Min TemperatureC') else None)
        self.mean_temperature = (int(readings.get('Mean TemperatureC'))
                                 if readings.get('Mean TemperatureC') else None)
        self.max_humidity = (int(readings.get('Max Humidity'))
                             if readings.get('Max Humidity') else None)
        self.mean_humidity = (int(readings.get(' Mean Humidity'))
                              if readings.get(' Mean Humidity') else None)
        self.min_humidity = (int(readings.get(' Min Humidity'))
                             if readings.get(' Min Humidity') else None)


class WeatherResult:
    """"Data structure to hold the results calculated by calculation module"""
    def __init__(self, high_day='', lowest=0, low_day='',
                 highest=0, humid_day='', humidity=0):
        self.highest_reading = highest
        self.highest_day = low_day
        self.lowest_reading = lowest
        self.lowest_day = high_day
        self.humidity_reading = humidity
        self.humidity_day = humid_day


