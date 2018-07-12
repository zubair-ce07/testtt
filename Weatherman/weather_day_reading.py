class WeatherReading:
    def __init__(self, day):
        date = day.get('PKT') or day.get('PKST')
        self.year, self.month, self.day = [int(d) for d in date.split('-')]
        self.highest_temp = int(day["Max TemperatureC"])
        self.lowest_temp = int(day["Min TemperatureC"])
        self.mean_temp = int(day["Mean TemperatureC"])
        self.highest_hum = int(day["Max Humidity"])
        self.lowest_hum = int(day["Min Humidity"])
        self.mean_hum = int(day["Mean Humidity"])
