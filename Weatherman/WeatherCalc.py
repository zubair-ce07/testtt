class WeatherAnalyzer:

    @staticmethod
    def highest_avg_temp_of_month(data):
        max_temps = list(map(lambda x: x.highest_temp, data))
        return sum(max_temps) / len(max_temps)

    @staticmethod
    def lowest_avg_temp_of_month(data):
        min_temps = list(map(lambda x: x.lowest_temp, data))
        return sum(min_temps) / len(min_temps)

    @staticmethod
    def average_mean_humidity_of_month(data):
        mean_humidity_list = list(map(lambda x: x.mean_hum, data))
        return sum(mean_humidity_list) / len(mean_humidity_list)

    @staticmethod
    def highest_temp_of_year(data):
        max_temps = list(map(lambda x: x.highest_temp, data))
        return max_temps.index(max(max_temps))

    @staticmethod
    def lowest_temp_of_year(data):
        min_temps = list(map(lambda x: x.lowest_temp, data))
        return min_temps.index(min(min_temps))

    @staticmethod
    def highest_hum_of_year(data):
        max_humidity_list = list(map(lambda x: x.highest_hum, data))
        return max_humidity_list.index(max(max_humidity_list))
