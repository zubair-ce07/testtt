class WeatherRecord:

    def __init__(self, weather_reading_row):
        self.reading_date = weather_reading_row['PKT']
        self.max_temperature = weather_reading_row['Max TemperatureC']
        self.mean_temperature = weather_reading_row['Mean TemperatureC']
        self.min_temperature = weather_reading_row['Min TemperatureC']
        self.max_humidity = weather_reading_row['Max Humidity']
        self.mean_humidity = weather_reading_row['Mean Humidity']
        self.min_humidity = weather_reading_row['Min Humidity']
