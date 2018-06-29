import datetime


class WeatherData:
    def __init__(self, date, h_temperature, l_temperature, m_temperature,
                 max_humidity, mean_humidity):
        self.__date = date
        self.__highest_temperature = h_temperature
        self.__lowest_temperature = l_temperature
        self.__mean_temperature = m_temperature
        self.__max_humidity = max_humidity
        self.__mean_humidity = mean_humidity

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def highest_temperature(self):
        return self.__highest_temperature

    @highest_temperature.setter
    def highest_temperature(self, h_temperature):
        self.__highest_temperature = h_temperature

    @property
    def lowest_temperature(self):
        return self.__lowest_temperature

    @lowest_temperature.setter
    def lowest_temperature(self, l_temperature):
        self.__lowest_temperature = l_temperature

    @property
    def max_humidity(self):
        return self.__max_humidity

    @max_humidity.setter
    def max_humidity(self, max_humidity):
        self.__max_humidity = max_humidity

    @property
    def mean_humidity(self):
        return self.__mean_humidity

    @mean_humidity.setter
    def mean_humidity(self, mean_humidity):
        self.__mean_humidity = mean_humidity

    @property
    def mean_temperature(self):
        return self.__mean_temperature

    @mean_temperature.setter
    def mean_temperature(self, mean_temperature):
        self.__mean_temperature = mean_temperature

    def set_all_members(self, line):

        one_day_data = WeatherData._get_one_day_data(line)

        self.date = one_day_data["PKT"]
        self.highest_temperature = one_day_data[
            "Max TemperatureC"
        ]
        self.lowest_temperature = one_day_data[
            "Min TemperatureC"
        ]
        self.mean_temperature = one_day_data[
            "Mean TemperatureC"
        ]
        self.max_humidity = one_day_data[
            "Max Humidity"
        ]
        self.mean_humidity = one_day_data[
            "Min Humidity"
        ]

    @staticmethod
    def _get_one_day_data(line):
        daily_report = dict()

        for key in line.keys():
            if key == "PKT" or key == "PKST":
                date = line["PKT" if "PKT" == key else "PKST"].split("-")
                value = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                daily_report["PKT"] = value
            else:
                try:
                    value = int(line[key])
                except ValueError:
                    try:
                        value = float(line[key])
                    except ValueError:
                        value = "NA"

                daily_report[key.strip()] = value

        return daily_report
