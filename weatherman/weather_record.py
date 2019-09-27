class WeatherRecord:
    def __init__(self, max_temp, min_temp, max_humidity, mean_humidity, weather_record_date):
        self.weather_record = {
            'max_temperature': [int(max_temp_value) for max_temp_value in max_temp if max_temp is not ''],
            'min_temperature': [int(min_temp_value) for min_temp_value in min_temp if min_temp is not ''],
            'max_humidity': [int(max_humidity_value) for max_humidity_value in max_humidity if max_humidity is not ''],
            'mean_humidity': [int(mean_humidity_value) for mean_humidity_value in max_humidity if max_humidity is not ''],
            'weather_record_date': weather_record_date       
        }
