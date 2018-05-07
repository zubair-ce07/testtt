class weatherData:

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

    def initialize_monthly_data(self,monthly_highest_average,monthly_lowest_average,
                                monthly_average_mean_humidity,max_temperature_per_day,
                                min_temperature_per_day):
        self.monthly_highest_average = monthly_highest_average
        self.monthly_lowest_average = monthly_lowest_average
        self.monthly_average_mean_humidity = monthly_average_mean_humidity
        self.max_temperature_per_day = max_temperature_per_day
        self.min_temperature_per_day = min_temperature_per_day

    def initialize_yearly_data(self,yearly_highest_temperature,yearly_lowest_temperature,
                               yearly_highest_humidity,yearly_hightest_temperature_date,
                               yearly_lowest_temperature_date,yearly_highest_humidity_date):
        self.yearly_highest_temperature = yearly_highest_temperature
        self.yearly_lowest_temperature = yearly_lowest_temperature
        self.yearly_highest_humidity = yearly_highest_humidity
        self.yearly_hightest_temperature_date = yearly_hightest_temperature_date
        self.yearly_lowest_temperature_date = yearly_lowest_temperature_date
        self.yearly_highest_humidity_date = yearly_highest_humidity_date

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

    def get_monthly_max_readings (self):
        return self.max_temperature_per_day

    def get_monthly_min_readings (self):
        return self.min_temperature_per_day
