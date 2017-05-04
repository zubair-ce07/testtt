from monthweather import MonthWeatherModel
import helperfile
from datetime import datetime


def print_highest_and_lowest_average_for_month(file_name):
    month_model = MonthWeatherModel(file_name)

    print("\n")
    highest_average = month_model.find_average_for_attribute("max_temperature")
    print("Highest Average : " + str(round(highest_average)) + "C")

    lowest_average = month_model.find_average_for_attribute("min_temperature")
    print("Lowest Average : " + str(round(lowest_average)) + "C")

    mean_humidity_average = month_model.find_average_for_attribute("mean_humidity")
    print("Average Mean Humidity: " + str(round(mean_humidity_average)) + "%")
