class WeatherReading:

    def __init__(self, conditions):
        self.pkt = conditions.get('PKT', conditions.get('PKST'))
        self.max_temperature = int(conditions.get('Max TemperatureC')) \
            if conditions.get('Max TemperatureC') else None
        self.min_temperature = int(conditions.get('Min TemperatureC')) \
            if conditions.get('Min TemperatureC') else None
        self.mean_temperature = int(conditions.get('Mean TemperatureC')) \
            if conditions.get('Mean TemperatureC') else None
        self.max_humidity = int(conditions.get('Max Humidity')) \
            if conditions.get('Max Humidity') else None
        self.mean_humidity = int(conditions.get(' Mean Humidity')) \
            if conditions.get(' Mean Humidity') else None
        self.min_humidity = int(conditions.get(' Min Humidity')) \
            if conditions.get(' Min Humidity') else None


class ReportResult:
    """"Data structure to hold the results calculated by calculation module"""
    def __init__(self, min_day='', minimum=0, max_day='',
                 maximum=0, humid_day='', humidity=0):
        self.highest_reading = maximum
        self.highest_day = max_day
        self.lowest_reading = minimum
        self.lowest_day = min_day
        self.humidity_reading = humidity
        self.humidity_day = humid_day


