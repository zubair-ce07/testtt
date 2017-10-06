class DayWeather:
    def __init__(self, data):
        self.PKT = data['PKT'] if 'PKT' in data else data['PKST']
        self.max_temperature = data['Max TemperatureC']
        self.min_temperature = data['Min TemperatureC']
        self.max_humidity = data['Max Humidity']
        self.mean_humidity = data[' Mean Humidity']

    def get_day(self):
        return self.PKT.split('-')[2]

    def get_month(self):
        return self.PKT.split('-')[1]
