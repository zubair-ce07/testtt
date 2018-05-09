class WeatherAnalyzer:

    yearly_highest_temperature = -100
    yearly_lowest_temperature = 100
    yearly_highest_humidity = -100
    yearly_hightest_temperature_date = ''
    yearly_lowest_temperature_date = ''
    yearly_highest_humidity_date = ''
    monthly_highest_average = 0
    monthly_lowest_average = 0
    monthly_average_mean_humidity = 0
    max_temperature_per_day = []
    min_temperature_per_day = []
    total_days_count = 0

    def calculate_weather_averages(self):
        self.monthly_highest_average = int(self.monthly_highest_average / self.total_days_count)
        self.monthly_lowest_average = int(self.monthly_lowest_average / self.total_days_count)
        self.monthly_average_mean_humidity = int(self.monthly_average_mean_humidity / self.total_days_count)

    def initialize_monthly_weather(self,weather_record):
        for weather_reading in weather_record:
            if weather_reading is not '':
                date,highest_temperature,lowest_temperature,highest_humidity,mean_humidity = weather_reading
                self.max_temperature_per_day.append(int(highest_temperature))
                self.min_temperature_per_day.append(int(lowest_temperature))
                self.monthly_highest_average += int(highest_temperature)
                self.monthly_lowest_average += int(lowest_temperature)
                self.monthly_average_mean_humidity += int(mean_humidity)
                self.total_days_count += 1
        self.calculate_weather_averages()

    def initialize_yearly_weather(self,weather_record):
        for weather_reading in weather_record:
            if weather_reading is not '':
                date,max_temperature,min_temperature,max_humidity,mean_humidity = weather_reading
                self.update_max_temperature(max_temperature,date)
                self.update_min_temperature(min_temperature,date)
                self.update_max_humidity(max_humidity,date)

    def update_max_temperature(self,max_temperature,date):
        if int(max_temperature) > self.yearly_highest_temperature:
            self.yearly_highest_temperature = int(max_temperature)
            self.yearly_hightest_temperature_date = date

    def update_min_temperature(self,min_temperature,date):
        if int(min_temperature) < self.yearly_lowest_temperature:
            self.yearly_lowest_temperature = int(min_temperature)
            self.yearly_lowest_temperature_date = date

    def update_max_humidity(self,max_humidity,date):
        if int(max_humidity) > self.yearly_highest_humidity:
            self.yearly_highest_humidity = int(max_humidity)
            self.yearly_highest_humidity_date = date
