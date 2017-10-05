class DailyWeather:

    weather = {}

    def __init__(self):
        self.weather = {}

    def set_weather(self, data):
        if 'PKT' in data:
            self.weather['PKT'] = data['PKT']
        elif 'PKST' in data.keys():
            self.weather['PKT'] = data['PKST']
        self.weather['Max TemperatureC'] = data['Max TemperatureC']
        self.weather['Min TemperatureC'] = data['Min TemperatureC']
        self.weather['Max Humidity'] = data['Max Humidity']
        self.weather['Mean Humidity'] = data[' Mean Humidity']

