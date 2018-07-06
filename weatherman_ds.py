class WeatherReading:

    def __init__(self, conditions):
        self.pkt: str = None
        self.max_temperature: int = None
        self.min_temperature: int = None
        self.mean_temperature: int = None
        self.max_humidity: int = None
        self.mean_humidity: int = None
        self.min_humidity: int = None

        if conditions['PKT']:
            self.pkt = conditions['PKT']
        if conditions['Max TemperatureC']:
            self.max_temperature = int(conditions['Max TemperatureC'])
        if conditions['Min TemperatureC']:
            self.min_temperature = int(conditions['Min TemperatureC'])
        if conditions['Mean TemperatureC']:
            self.mean_temperature = int(conditions['Mean TemperatureC'])
        if conditions['Max Humidity']:
            self.max_humidity = int(conditions['Max Humidity'])
        if conditions[' Mean Humidity']:
            self.mean_humidity = int(conditions[' Mean Humidity'])


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


