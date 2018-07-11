from statistics import mean


class Computer:

    @staticmethod
    def result_e(data):
        yearly_max_temperature = max(data, key=lambda wr: wr.max_temperature)
        yearly_min_temperature = min(data, key=lambda wr: wr.max_temperature)
        yearly_max_humidity = max(data, key=lambda wr: wr.max_humidity)
        return [yearly_max_temperature, yearly_min_temperature, yearly_max_humidity]

    @staticmethod
    def result_a(data):
        max_avg_temperature = max(data, key=lambda wr: wr.mean_temperature)
        min_avg_temperature = min(data, key=lambda wr: wr.mean_temperature)
        avg_mean_humidity = int(mean(wr.mean_humidity for wr in data if wr.mean_humidity is not None))
        avg_mean_humidity = next((wr for wr in data if wr.mean_humidity == avg_mean_humidity), None)
        return [max_avg_temperature, min_avg_temperature, avg_mean_humidity]

    @staticmethod
    def result_c(data):
        return data
