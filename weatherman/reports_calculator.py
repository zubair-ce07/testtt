class ReportsCalculator:

    @staticmethod
    def extreme_values(data):
        """Returns dictionary containing maximum temperature, minimum temperature and most humid day """

        max_temperature = max(data['max_temperature'])
        min_temperature = min(data['min_temperature'])
        max_humidity = max(data['max_humidity'])

        max_temperature_index = data['max_temperature'].index(max_temperature)
        min_temperature_index = data['min_temperature'].index(min_temperature)
        max_humidity_index = data['max_humidity'].index(max_humidity)

        max_temp_date = data['max_temp_date'][max_temperature_index]
        min_temp_date = data['min_temp_date'][min_temperature_index]
        max_humidity_date = data['max_humidity_date'][max_humidity_index]

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
    def average_values(data):
        """Returns dictionary containing average values of maximum temperature, minimum temperature and mean
            humidity
         """

        average_max_temp = sum(data['max_temperature']) // len(data['max_temperature'])
        average_min_temp = sum(data['min_temperature']) // len(data['min_temperature'])
        average_mean_humidity = sum(data['mean_humidity']) // len(data['mean_humidity'])

        averages = {
            'avg_max_temperature': average_max_temp,
            'avg_min_temperature': average_min_temp,
            'avg_mean_humidity': average_mean_humidity
        }

        return averages
