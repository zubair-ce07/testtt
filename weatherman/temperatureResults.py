

class TempReading:
    def __init__(self, date_high_temp, high_temp, date_low_temp, low_temp, date_humidity, humidity, mean_humidity):
        self.date_high_temp = date_high_temp
        self.high_temp = None
        self.date_low_temp = date_low_temp
        self.low_temp = None
        self.date_humidity=date_humidity
        self.humidity = None
        self.mean_humidity = None
        if high_temp:
            self.high_temp = int(high_temp)
        if low_temp:
            self.low_temp = int(low_temp)
        if humidity:
            self.humidity = int(humidity)
        if mean_humidity:
            self.mean_humidity = int(mean_humidity)
