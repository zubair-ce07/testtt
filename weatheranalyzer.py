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
        self.total_days_count = 0


    def calculate_weather_averages(self):
        self.highest_average = int(self.highest_average / self.total_days_count)
        self.lowest_average = int(self.lowest_average / self.total_days_count)
        self.average_mean_humidity = int(self.average_mean_humidity / self.total_days_count)


    def initialize_weather_record(self, weather_record):
        for weather_reading in weather_record:
            date, max_temperature, min_temperature, max_humidity, mean_humidity = weather_reading
            self.max_temperatures.append(int(max_temperature))
            self.min_temperatures.append(int(min_temperature))
            self.max_humidity.append(int(max_humidity))
            self.weather_date.append(date)
            self.highest_average += int(max_temperature)
            self.lowest_average += int(min_temperature)
            self.average_mean_humidity += int(mean_humidity)
            self.total_days_count += 1
        self.calculate_weather_averages()
        self.update_max_temperature()
        self.update_min_temperature()
        self.update_max_humidity()


    def update_max_temperature(self):
        self.highest_temperature = max(self.max_temperatures)
        self.hightest_temperature_date = self.weather_date[self.max_temperatures.index(int(self.highest_temperature))]


    def update_min_temperature(self):
        self.lowest_temperature = min(self.min_temperatures)
        self.lowest_temperature_date = self.weather_date[self.min_temperatures.index(int(self.lowest_temperature))]


    def update_max_humidity(self):
        self.highest_humidity = max(self.max_humidity)
        self.highest_humidity_date = self.weather_date[self.max_humidity.index(int(self.highest_humidity))]
