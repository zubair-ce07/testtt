from statistics import mean


class Computer:
    def __init__(self, data):
        self.__record = data

    def result_e(self, year):
        monthly_max_temperatures = []
        monthly_min_temperatures = []
        monthly_max_humidity = []
        for k, v in self.__record[year].items():
            monthly_max_temperatures.append(max(v, key=lambda wr: wr.max_temperature))
            monthly_min_temperatures.append(min(v, key=lambda wr: wr.min_temperature))
            monthly_max_humidity.append(max(v, key=lambda wr: wr.max_humidity))
        yearly_max_temperature = max(monthly_max_temperatures, key=lambda wr: wr.max_temperature)
        yearly_min_temperature = min(monthly_min_temperatures, key=lambda wr: wr.max_temperature)
        yearly_max_humidity = max(monthly_max_humidity,key=lambda wr: wr.max_humidity)
        return [yearly_max_temperature, yearly_min_temperature, yearly_max_humidity]

    def result_a(self, month, year):
        month = self.__record[year][month[:3]]
        max_avg_temperature = max(month, key=lambda wr: wr.mean_temperature)
        min_avg_temperature = min(month, key=lambda wr: wr.mean_temperature)
        avg_mean_humidity = int(mean(wr.mean_humidity for wr in month if wr.mean_humidity is not None))
        avg_mean_humidity = next((wr for wr in month if wr.mean_humidity == avg_mean_humidity), None)
        return [max_avg_temperature, min_avg_temperature, avg_mean_humidity]

    def result_c(self, month, year):
        return self.__record[year][month[:3]]
