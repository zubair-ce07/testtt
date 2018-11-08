from datetime import datetime


class WeatherRecords:
    """ Class for holding the only required data for each instance """

    def __init__(self, record):
        self.max_temperature = int(record["Max TemperatureC"])
        self.min_temperature = int(record["Min TemperatureC"])
        self.max_humidity = int(record["Max Humidity"])
        self.min_humidity = int(record[" Min Humidity"])
        self.mean_humidity = int(record[" Mean Humidity"])
        raw_date = record.get("PKT") or record.get("PKST")
        self.date = datetime.strptime(raw_date, "%Y-%m-%d")
