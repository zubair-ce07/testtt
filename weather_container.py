from datetime import datetime


class RecordHolder:
    def __init__(self, data):

        self.maximum_temp = int(data["Max TemperatureC"])
        self.minimum_temp = int(data["Min TemperatureC"])
        self.average_humidity = int(data[" Mean Humidity"])
        self.maximum_humidity = int(data["Max Humidity"])
        date = data.get("PKT") or data.get("PKST")
        self.date = datetime.strptime(date, "%Y-%m-%d")
