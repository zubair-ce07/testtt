class ResultContainer:
    """This class is used as a data structure to store all the
    result values"""
    def __init__(self, h_temperature, h_temperature_day, l_temperature,
                 l_temperature_day, h_humidity, m_humid_day, r_type):
        self.__highest_temperature = h_temperature
        self.__highest_temperature_day = h_temperature_day
        self.__lowest_temperature = l_temperature
        self.__lowest_temperature_day = l_temperature_day
        self.__highest_humidity = h_humidity
        self.__most_humid_day = m_humid_day
        self.__result_type = r_type
        self.temperature_list = []

    def get_highest_temperature(self):
        return self.__highest_temperature

    def get_highest_temperature_day(self):
        return self.__highest_temperature_day

    def get_lowest_temperature(self):
        return self.__lowest_temperature

    def get_lowest_temperature_day(self):
        return self.__lowest_temperature_day

    def get_highest_humidity(self):
        return self.__highest_humidity

    def get_most_humid_day(self):
        return self.__most_humid_day

    def get_result_type(self):
        return self.__result_type

    def set_highest_temperature(self, h_temperature):
        self.__highest_temperature = h_temperature

    def set_highest_temperature_day(self, h_temperature_day):
        self.__highest_temperature_day = h_temperature_day

    def set_lowest_temperature(self, l_temperature):
        self.__lowest_temperature = l_temperature

    def set_lowest_temperature_day(self, l_temperature_day):
        self.__lowest_temperature_day = l_temperature_day

    def set_highest_humidity(self, h_humidity):
        self.__highest_humidity = h_humidity

    def set_most_humid_day(self, m_humid_day):
        self.__most_humid_day = m_humid_day

    def set_result_type(self, r_type):
        self.__result_type = r_type
