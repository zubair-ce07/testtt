class weatherAnalyzer:

    def __init__(self):
        self.yearly_highest_temperature = -100
        self.yearly_lowest_temperature = 100
        self.yearly_highest_humidity = -100
        self.yearly_hightest_temperature_date = ''
        self.yearly_lowest_temperature_date = ''
        self.yearly_highest_humidity_date = ''
        self.monthly_highest_average = 0
        self.monthly_lowest_average = 0
        self.monthly_average_mean_humidity = 0
        self.max_temperature_per_day = []
        self.min_temperature_per_day = []
        self.total_days_count = 0

    def initialize_monthly_weather(self,weather_record):
        for index,value in enumerate(weather_record):
            if value is not '':
                date,highest_temperature,lowest_temperature,highest_humidity,mean_humidity = value
                self.max_temperature_per_day.append(int(highest_temperature))
                self.min_temperature_per_day.append(int(lowest_temperature))
                self.monthly_highest_average += int(highest_temperature)
                self.monthly_lowest_average += int(lowest_temperature)
                self.monthly_average_mean_humidity += int(mean_humidity)
                self.total_days_count += 1
        self.calculate_weather_averages()

    def calculate_weather_averages(self):
        self.monthly_highest_average = int(self.monthly_highest_average / self.total_days_count)
        self.monthly_lowest_average = int(self.monthly_lowest_average / self.total_days_count)
        self.monthly_average_mean_humidity = int(self.monthly_average_mean_humidity / self.total_days_count)

    def initialize_yearly_weather(self,weather_record):
        for index,value in enumerate(weather_record):
            if value is not 0 or None:
                date,max_temperature,min_temperature,max_humidity,mean_humidity = value
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

    def get_monthly_weather_details (self):
        monthly_weather_report = {"monthly_highest_average" : self.monthly_highest_average,
                                  "monthly_lowest_average" : self.monthly_lowest_average,
                                  "monthly_average_mean_humidity" : self.monthly_average_mean_humidity }
        return monthly_weather_report

    def get_yearly_weather_details (self):
        yearly_weather_details = {"highest_annual_temperature": self.yearly_highest_temperature,
                                  "highest_annual_temperature_date": self.yearly_hightest_temperature_date,
                                  "lowest_annual_temperature": self.yearly_lowest_temperature,
                                  "lowest_annual_temperature_date": self.yearly_lowest_temperature_date,
                                  "highest_annual_humidity": self.yearly_highest_humidity,
                                  "highest_annual_humidity_date": self.yearly_highest_humidity_date,}
        return yearly_weather_details
