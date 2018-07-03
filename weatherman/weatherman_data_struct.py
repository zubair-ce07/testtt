from datetime import datetime


class Record:
    """
    Data Structure to store the Weather data
    """
    def __init__(self, data):
        self.date = datetime.strptime(data["PKT"], "%Y-%m-%d")
        self.max_temperature = int(data["Max TemperatureC"]) if data["Max TemperatureC"].isdigit() else None
        self.min_temperature = int(data["Min TemperatureC"]) if data["Min TemperatureC"].isdigit() else None
        self.max_humidity = int(data["Max Humidity"]) if data["Max Humidity"].isdigit() else None
        self.mean_humidity = int(data[" Mean Humidity"]) if data[" Mean Humidity"].isdigit() else None
