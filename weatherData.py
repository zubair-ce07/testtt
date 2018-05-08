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

    def initialize_monthly_data(self,weather_data):
        total_days_count = 0
        date = ''
        for index,value in enumerate(weather_data):
            if value is not 0:
                date,highest_temperature,lowest_temperature,highest_humidity,mean_humidity = value
                self.max_temperature_per_day.append(int(highest_temperature))
                self.min_temperature_per_day.append(int(lowest_temperature))

                self.monthly_highest_average += int(highest_temperature)
                self.monthly_lowest_average += int(lowest_temperature)
                self.monthly_average_mean_humidity += int(mean_humidity)
                total_days_count += 1

        self.monthly_highest_average = int(self.monthly_highest_average / total_days_count)
        self.monthly_lowest_average = int(self.monthly_lowest_average / total_days_count)
        self.monthly_average_mean_humidity = int(self.monthly_average_mean_humidity / total_days_count)

    def initialize_yearly_data(self,weather_data):
        for index,value in enumerate(weather_data):
            if value is not 0 or None:
                date,highest_temperature,lowest_temperature,highest_humidity,mean_humidity = value

                if int(highest_temperature) > self.yearly_highest_temperature:
                    self.yearly_highest_temperature = int(highest_temperature)
                    self.yearly_hightest_temperature_date = date

                if int(lowest_temperature) < self.yearly_lowest_temperature:
                    self.yearly_lowest_temperature = int(lowest_temperature)
                    self.yearly_lowest_temperature_date = date

                if int(highest_humidity) > self.yearly_highest_humidity:
                    self.yearly_highest_humidity = int(highest_humidity)
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

    def get_monthly_max_readings (self):
        return self.max_temperature_per_day

    def get_monthly_min_readings (self):
        return self.min_temperature_per_day
