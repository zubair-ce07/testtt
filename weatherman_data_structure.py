from datetime import datetime


class ReadingsHolder:

    def __init__(self, features):
        self.pkt = features.get('PKT') or features.get('PKST')
        self.pkt = datetime.strptime(self.pkt, '%Y-%m-%d')
        self.max_temp = int(features.get('Max TemperatureC'))
        self.min_temp = int(features.get('Min TemperatureC'))
        self.mean_temp = int(features.get('Mean TemperatureC'))
        self.max_humidity = int(features.get('Max Humidity'))
        self.min_humidity = int(features.get(' Min Humidity'))
        self.mean_humidity = int(features.get(' Mean Humidity'))


class Colors:

    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    RESET = "\u001b[0m"
