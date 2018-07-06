class WeatherAnalyzer:

    @staticmethod
    def highest_avg_temp_of_month(data):
        return sum(x.highest_temp for x in data) / len(data)

    @staticmethod
    def lowest_avg_temp_of_month(data):
        return sum(x.lowest_temp for x in data) / len(data)

    @staticmethod
    def average_mean_humidity_of_month(data):
        return sum(x.mean_hum for x in data) / len(data)

    @staticmethod
    def highest_temp_of_year(data):
        return max(data, key=lambda x: x.highest_temp)

    @staticmethod
    def lowest_temp_of_year(data):
        return min(data, key=lambda x: x.lowest_temp)

    @staticmethod
    def highest_hum_of_year(data):
        return max(data, key=lambda x: x.highest_hum)