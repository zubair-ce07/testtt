class WeatherData:
    def __init__(self, date, h_temperature, l_temperature, m_temperature, max_humidity, mean_humidity):
        self.date = date
        self.highest_temperature = h_temperature
        self.lowest_temperature = l_temperature
        self.mean_temperature = m_temperature
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
