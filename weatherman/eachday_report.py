"""This file contains the EachDayReport that calculates the
the each day stats and print the each day report"""


class EachDayReport:

    def __init__(self):
        self.max_temp = 0
        self.min_temp = 0
        self.date = ''

    def print_eachday_report(self, weather_dict):
        """This method calculates the each day report
        and print as required"""

        if (weather_dict["Max TemperatureC"] and
                weather_dict["Min TemperatureC"]):
            self.max_temp = int(weather_dict["Max TemperatureC"])
            self.min_temp = int(weather_dict["Min TemperatureC"])
            self.date = str(weather_dict["PKT"]).split("-")[2]
            if len(self.date) == 1:
                self.date = "0" + self.date

            print("\33[95m" + self.date, end=" ")
            print("\33[31m" + "+" * self.max_temp, end=" ")
            print("\33[95m" + str(self.max_temp) + "C")

            print("\33[95m" + self.date, end=" ")
            print("\33[94m" + "+" * self.min_temp, end=" ")
            print("\33[95m" + str(self.min_temp) + "C" + "\33[0m")

    def print_eachday_report_bonus(self, weather_dict):
        """This method calculates the each day report
        and print as required. it is the bonus taks"""

        if (weather_dict["Max TemperatureC"] and
                weather_dict["Min TemperatureC"]):
            self.max_temp = int(weather_dict["Max TemperatureC"])
            self.min_temp = int(weather_dict["Min TemperatureC"])
            self.date = str(weather_dict["PKT"]).split("-")[2]
            if len(self.date) == 1:
                self.date = "0" + self.date

            print("\33[95m" + self.date, end=" ")
            print("\33[94m" + "+" * self.min_temp, end="")
            print("\33[31m" + "+" * self.max_temp, end=" ")
            print("\33[95m" + str(self.min_temp) + "C", end=" - ")
            print("\33[95m" + str(self.max_temp) + "C" + "\33[0m")
