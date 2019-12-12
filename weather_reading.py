class WeatherReading:

    def __init__(self, weather_reading_row):
        self.reading_date = weather_reading_row['PKT']
        self.max_temperature = weather_reading_row['MAX_TEMP']
        self.mean_temperature = weather_reading_row['MEAN_TEMP']
        self.min_temperature = weather_reading_row['MEAN_TEMP']
        self.max_humidity = weather_reading_row['MAX_HUMIDITY']
        self.mean_humidity = weather_reading_row['MEAN_HUMIDITY']
        self.min_humidity = weather_reading_row['MIN_HUMIDITY']
