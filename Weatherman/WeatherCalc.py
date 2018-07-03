class WeatherCalc:

    @staticmethod
    def highest_avg_temp_of_month(data):
        total = 0
        counter = 0
        for data_segments in data:
            for data_segment in data_segments:
                if data_segment.highest_temp != -100:
                    total += data_segment.highest_temp
                    counter += 1
        return total / counter

    @staticmethod
    def lowest_avg_temp_of_month(data):
        total = 0
        counter = 0
        for data_segments in data:
            for data_segment in data_segments:
                if data_segment.lowest_temp != -100:
                    total += data_segment.lowest_temp
                    counter += 1
        return total / counter

    @staticmethod
    def average_mean_humidity_of_month(data):
        total = 0
        counter = 0
        for data_segments in data:
            for data_segment in data_segments:
                if data_segment.mean_hum != -100:
                    total += data_segment.mean_hum
                    counter += 1
        return total/counter

    @staticmethod
    def highest_temp_of_year(data):
        highest_temp = 0
        index = 0
        index1 = 0
        for data_segments in data:
            for data_segment in data_segments:
                if data_segment.highest_temp > highest_temp:
                    highest_temp = data_segment.highest_temp
                    index1 = data_segments.index(data_segment)
                    index = data.index(data_segments)
        return [index, index1]

    @staticmethod
    def lowest_temp_of_year(data):
        lowest_temp = 100
        index = 0
        index1 = 0
        for data_segments in data:
            for data_segment in data_segments:
                if data_segment.lowest_temp < lowest_temp:
                    lowest_temp = data_segment.lowest_temp
                    index1 = data_segments.index(data_segment)
                    index = data.index(data_segments)
        return [index, index1]

    @staticmethod
    def highest_hum_of_year(data):
        highest_hum = 0
        index = 0
        index1 = 0
        for data_segments in data:
            for data_segment in data_segments:
                if data_segment.highest_hum > highest_hum:
                    highest_hum = data_segment.highest_hum
                    index1 = data_segments.index(data_segment)
                    index = data.index(data_segments)
        return [index, index1]
