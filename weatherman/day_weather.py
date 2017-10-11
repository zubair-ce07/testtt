class DayWeatherRecord:
    def __init__(self, raw_day_weather):
        self.date = raw_day_weather['PKT'] if 'PKT' in raw_day_weather else raw_day_weather['PKST']
        self.max_temperature = raw_day_weather['Max TemperatureC']
        self.min_temperature = raw_day_weather['Min TemperatureC']
        self.max_humidity = raw_day_weather['Max Humidity']
        self.mean_humidity = raw_day_weather[' Mean Humidity']

    def get_day_number(self):
        return int(self.date.split('-')[2])

    def get_month_number(self):
        return int(self.date.split('-')[1])
