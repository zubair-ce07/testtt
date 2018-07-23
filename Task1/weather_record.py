import datetime


class WeatherRecord:
    def __init__(self, weather_record):
        date_string = weather_record.get("PKT", weather_record.get("PKST", None))
        self.date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        self.highest_temperature = int(weather_record["Max TemperatureC"])
        self.lowest_temperature = int(weather_record["Min TemperatureC"])
        self.mean_temperature = float(weather_record["Mean TemperatureC"])
        self.max_humidity = float(weather_record["Max Humidity"])
        self.mean_humidity = float(weather_record[" Min Humidity"])
