class DayWeather:
    def __init__(self, day_weather):
        self.date = day_weather['PKT'] if 'PKT' in day_weather else day_weather['PKST']
        self.max_temperature = int(day_weather['Max TemperatureC'])
        self.min_temperature = int(day_weather['Min TemperatureC'])
        self.max_humidity = int(day_weather['Max Humidity'])
        self.mean_humidity = int(day_weather[' Mean Humidity'])

    def get_day_number(self):
        return int(self.date.split('-')[2])

    def get_month_number(self):
        return int(self.date.split('-')[1])
