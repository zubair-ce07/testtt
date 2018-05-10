class WeatherAnalyzer:

    def __init__ (self):
        self.highest_temperature = -100
        self.lowest_temperature = 100
        self.highest_humidity = -100
        self.hightest_temperature_date = ''
        self.lowest_temperature_date = ''
        self.highest_humidity_date = ''
        self.highest_average = 0
        self.lowest_average = 0
        self.average_mean_humidity = 0
        self.max_temperatures = []
        self.min_temperatures = []
        self.max_humidity = []
        self.weather_date = []
        self.weather_records = []
        self.total_days_count = 0


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
        for weather_reading in self.weather_records:
            date, max_temperature, min_temperature, max_humidity, mean_humidity = weather_reading
            if int(max_temperature) > self.highest_temperature:
                self.highest_temperature = int(max_temperature)
                self.hightest_temperature_date = date
            if int(min_temperature) < self.lowest_temperature:
                self.lowest_temperature = int(min_temperature)
                self.lowest_temperature_date = date
            if int(max_humidity) > self.highest_humidity:
                self.highest_humidity = int(max_humidity)
                self.highest_humidity_date = date
