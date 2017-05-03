from MonthWeather import MonthWeatherModel
import HelperFile
from datetime import datetime


def print_highest_and_lowest_average_for_month(input_string):
    try:
        components = datetime.strptime(input_string, '%Y' + '/' + '%m')
    except ValueError:
        print("Data for", input_string, "is not available")
        return

    year = str(components.year)  # year = "2009"
    month = components.month  # month = "Jan"
    month = HelperFile.get_month_abbreviation(month)

    file_name = "Murree_weather_" + year + "_" + month + ".txt"

    if HelperFile.does_weather_file_exist(file_name) == False:
        print("Data for", input_string, "is not available")
        return

    month_model = MonthWeatherModel(file_name)

    print("\n")

    highest_average = month_model.find_average_for_attribute("MaxTemperatureC")
    print("Highest Average : " + str(round(highest_average)) + "C")

    lowest_average = month_model.find_average_for_attribute("MinTemperatureC")
    print("Lowest Average : " + str(round(lowest_average)) + "C")

    mean_humidity_average = month_model.find_average_for_attribute("MeanHumidity")
    print("Average Mean Humidity: " + str(round(mean_humidity_average)) + "%")
