class WeatherRecord:

    
    def __init__(self, max_temp, min_temp, max_humidity, mean_humidity,max_temp_date, min_temp_date, max_humidity_date):
        self.weather_record = {
            'max_temperature': max_temp,
            'min_temperature': min_temp,
            'max_humidity': max_humidity,
            'mean_humidity': mean_humidity,
            'max_temp_date': max_temp_date,
            'min_temp_date': min_temp_date,
            'max_humidity_date': max_humidity_date
        }