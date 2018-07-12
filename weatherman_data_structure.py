from enum import Enum


class ReadingsHolder:

    def __init__(self, features):
        if 'PKT' in features.keys():
            self.pkt = features.get('PKT')
        else:
            self.pkt = features.get('PKST')
        self.max_temp = int(features.get('Max TemperatureC'))
        self.min_temp = int(features.get('Min TemperatureC'))
        self.mean_temp = int(features.get('Mean TemperatureC'))
        self.max_humidity = int(features.get('Max Humidity'))
        self.min_humidity = int(features.get(' Min Humidity'))
        self.mean_humidity = int(features.get(' Mean Humidity'))


class CalculationHolder:

    def __init__(self, **weather_readings):
        self.maximum_temp = weather_readings.get('max_temp', 0)
        self.minimum_temp = weather_readings.get('min_temp', 0)
        self.maximum_humidity = weather_readings.get('max_humidity', 0)
        self.maximum_temp_day = weather_readings.get('max_temp_day', '')
        self.minimum_temp_day = weather_readings.get('min_temp_day', '')
        self.maximum_humidity_day = weather_readings.get('max_humid_day', '')
        self.max_mean_temp = weather_readings.get('max_mean_temp', 0)
        self.min_mean_temp = weather_readings.get('min_mean_temp', 0)
        self.average_mean_humidity = weather_readings.get('avg_mean_humidity',
                                                          0)


class Colors:

    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    RESET = "\u001b[0m"
