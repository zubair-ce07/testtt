class ReportsCalculator:
    
        
    @staticmethod
    def calculate_min_max(weather_data):
        
        """Returns dictionary containing maximum temperature, minimum temperature and most humid day """        
        max_temperature = max(weather_data['max_temperature'])        
        min_temperature = min(weather_data['min_temperature'])
        max_humidity = max(weather_data['max_humidity'])

        max_temperature_index = weather_data['max_temperature'].index(max_temperature)
        min_temperature_index = weather_data['min_temperature'].index(min_temperature)
        max_humidity_index = weather_data['max_humidity'].index(max_humidity)

        max_temp_date = weather_data['max_temp_date'][max_temperature_index]
        min_temp_date = weather_data['min_temp_date'][min_temperature_index]
        max_humidity_date = weather_data['max_humidity_date'][max_humidity_index]

        extremes = {
            'max_temperature': max_temperature,
            'max_humidity': max_humidity,
            'min_temperature': min_temperature,
            'max_temp_date': max_temp_date,
            'min_temp_date': min_temp_date,
            'max_humidity_date': max_humidity_date
        }

        return extremes

    @staticmethod
    def calculate_averages(weather_data):
        """Returns dictionary containing average values of maximum temperature, minimum temperature and mean
            humidity
         """

        average_max_temp = sum(weather_data['max_temperature']) // len(weather_data['max_temperature'])
        average_min_temp = sum(weather_data['min_temperature']) // len(weather_data['min_temperature'])
        average_mean_humidity = sum(weather_data['mean_humidity']) // len(weather_data['mean_humidity'])

        averages = {
            'avg_max_temperature': average_max_temp,
            'avg_min_temperature': average_min_temp,
            'avg_mean_humidity': average_mean_humidity
        }

        return averages