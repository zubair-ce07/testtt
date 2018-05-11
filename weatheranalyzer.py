import operator


class WeatherAnalyzer:

    def __init__ (self, weather_record):
        self.weather_record = weather_record

    def test(self):
        for value in self.weather_record:
            print (value)
        # print (len(self.weather_record))

    def initialize_weather_record(self, weather_record):
        for weather_reading in weather_record:
            date, max_temperature, min_temperature, max_humidity, mean_humidity = weather_reading
            self.weather_records.append(weather_reading)
            self.max_temperatures.append(int(max_temperature))
            self.min_temperatures.append(int(min_temperature))
            self.max_humidity.append(int(max_humidity))
            self.weather_date.append(date)
            self.highest_average += int(max_temperature)
            self.lowest_average += int(min_temperature)
            self.average_mean_humidity += int(mean_humidity)
            self.total_days_count += 1
        self.highest_average = int(self.highest_average / self.total_days_count)
        self.lowest_average = int(self.lowest_average / self.total_days_count)
        self.average_mean_humidity = int(self.average_mean_humidity / self.total_days_count)


    def calculate_weather_extremes(self):
        self.max_weather = max(self.weather_record, key = lambda index: index.max_temp)
        self.min_weather = min(self.weather_record, key = lambda index: index.min_temp)
        self.max_humidity = max(self.weather_record, key = lambda index: index.max_humidity)

    def calculat_weather_averages(self):
        self.max_temp_avrg = sum(self.weather_record, key = lambda index: index.max_temp) / len(self.weather_record)
        self.min_temp_avrg = sum(self.weather_record, key = lambda index: index.min_temp) / len(self.weather_record)
        self.max_humidity_avrg = sum(self.weather_record, key = lambda index: index.mean_humidity) / len(self.weather_record)
