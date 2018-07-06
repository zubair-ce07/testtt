class WeatherAnalyzer:

    @staticmethod
    def highest_avg_temp_of_month(weather_readings):
        return sum(x.highest_temp for x in weather_readings) / len(weather_readings)

    @staticmethod
    def lowest_avg_temp_of_month(weather_readings):
        return sum(x.lowest_temp for x in weather_readings) / len(weather_readings)

    @staticmethod
    def average_mean_humidity_of_month(weather_readings):
        return sum(x.mean_hum for x in weather_readings) / len(weather_readings)

    @staticmethod
    def highest_temp_of_year(weather_readings):
        return max(weather_readings, key=lambda x: x.highest_temp)

    @staticmethod
    def lowest_temp_of_year(weather_readings):
        return min(weather_readings, key=lambda x: x.lowest_temp)

    @staticmethod
    def highest_hum_of_year(weather_readings):
        return max(weather_readings, key=lambda x: x.highest_hum)
