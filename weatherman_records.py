from datetime import datetime


class Colors:
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    RESET = "\033[1;39m"


class DailyRecords:
    def __init__(self, row):
        date = row.get('PKT') or row.get('PKST')
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.max_temperature = int(row.get('Max TemperatureC'))
        self.min_temperature = int(row.get('Min TemperatureC'))
        self.max_humidity = int(row.get('Max Humidity'))
        self.mean_humidity = int(row.get(' Mean Humidity'))
