from datetime import datetime


class WeatherReading:
    """Structure to store weather readings data"""

    def _parse_numeric_value(self, row, key):
        value = row.get(key, "")
        return int(value) if value.isdigit() else None

    def __init__(self, readings_row):
        date = readings_row.get("PKT", readings_row.get("PKST"))
        self.date = datetime.strptime(date, "%Y-%m-%d")

        self.max_temperature = self._parse_numeric_value(readings_row, "Max TemperatureC")
        self.mean_temperature= self._parse_numeric_value(readings_row, "Mean TemperatureC")
        self.min_temperature= self._parse_numeric_value(readings_row, "Min TemperatureC")
        self.max_humidity= self._parse_numeric_value(readings_row, "Max Humidity")
        self.mean_humidity= self._parse_numeric_value(readings_row, " Mean Humidity")
        self.min_humidity= self._parse_numeric_value(readings_row, " Min Humidity")
