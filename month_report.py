"""This file contains the class of MonthReport
to calculate and print the monthly stats of weather"""


class MonthReport:

    def __init__(self):
        self.sum_max_temp = 0
        self.avg_max_temp = 0
        self.max_temp_count = 0

        self.sum_min_temp = 0
        self.avg_min_temp = 0
        self.min_temp_count = 0

        self.sum_mean_humidity = 0
        self.avg_mean_humidity = 0
        self.mean_humidity_count = 0

    def cal_sum_of_data(self, weather_dict):
        """This method calculates the sum of weather
        data"""

        if weather_dict["Max TemperatureC"]:
            self.sum_max_temp += int(weather_dict["Max TemperatureC"])
            self.max_temp_count += 1
        if weather_dict["Min TemperatureC"]:
            self.sum_min_temp += int(weather_dict["Min TemperatureC"])
            self.min_temp_count += 1
        if weather_dict["Max Humidity"]:
            self.sum_mean_humidity += int(weather_dict["Mean Humidity"])
            self.mean_humidity_count += 1

    def take_avg_of_data(self):
        """This method takes the average of preivously summed
        data"""

        self.avg_max_temp = self.sum_max_temp // self.max_temp_count
        self.avg_min_temp = self.sum_min_temp // self.min_temp_count
        self.avg_mean_humidity = (
            self.sum_mean_humidity // self.mean_humidity_count
            )

    def print_month_report(self):
        """This method prints the monthly report as
        required"""

        print("Highest Average: " + str(self.avg_max_temp) + "C")
        print("Lowest Average: " + str(self.avg_min_temp) + "C")
        print("Average Mean Humidity: " + str(self.avg_mean_humidity) + "%")
