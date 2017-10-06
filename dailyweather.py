class DailyWeather:
    PKT = ''
    max_temperature = 0
    min_temperature = 0
    max_humidity = 0
    mean_humidity = 0

    def __init__(self):
        self.PKT = ''
        self.max_temperature = 0
        self.min_temperature = 0
        self.max_humidity = 0
        self.mean_humidity = 0

    def set_weather(self, data):
        self.PKT = data['PKT'] if 'PKT' in data else data['PKST']
        self.max_temperature = data['Max TemperatureC']
        self.min_temperature = data['Min TemperatureC']
        self.max_humidity = data['Max Humidity']
        self.mean_humidity = data[' Mean Humidity']
