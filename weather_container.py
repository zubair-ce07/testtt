from datetime import datetime


class RecordHolder:
    def __init__(self, data):

        self.max_temp = int(data["Max TemperatureC"])
        self.min_temp = int(data["Min TemperatureC"])
        self.avg_humidity = int(data[" Mean Humidity"])
        self.max_humidity = int(data["Max Humidity"])
        date = data.get("PKT", data.get("PKST"))
        self.date = datetime.strptime(date, "%Y-%m-%d")
