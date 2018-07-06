class WeatherResult:
    def __init__(self, h_temperature="", a_h_temperature="", h_temperature_day="", l_temperature="",
                 a_l_temperature="", l_temperature_day="", h_humidity="", m_humid_day="",
                 mean_humidity="", daily_temperatures=None):
        self.highest_temperature = h_temperature
        self.average_highest_temperature = a_h_temperature
        self.highest_temperature_day = h_temperature_day
        self.lowest_temperature = l_temperature
        self.average_lowest_temperature = a_l_temperature
        self.lowest_temperature_day = l_temperature_day
        self.highest_humidity = h_humidity
        self.most_humid_day = m_humid_day
        self.mean_humidity = mean_humidity

        if daily_temperatures:
            self.daily_temperatures = daily_temperatures
        else:
            self.daily_temperatures = []
