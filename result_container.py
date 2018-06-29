class ResultContainer:
    def __init__(self, h_temperature, h_temperature_day, l_temperature,
                 l_temperature_day, h_humidity, m_humid_day):
        self.highest_temperature = h_temperature
        self.highest_temperature_day = h_temperature_day
        self.lowest_temperature = l_temperature
        self.lowest_temperature_day = l_temperature_day
        self.highest_humidity = h_humidity
        self.most_humid_day = m_humid_day
        self.temperature_list = []
