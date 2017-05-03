import operator
import os
from MonthWeather import MonthWeatherModel
from datetime import datetime


def highest_lowest_temperature_and_humidity(year):
    # year = input("Please enter year: ")
    year_in_int = 0
    try:
        year_in_int = int(year)
    except ValueError:
        year_in_int = 1
        # do nothing

    if year_in_int < 2004 or year_in_int > 2016:
        print("Data for year", year, "is not available")
        return

    attribute = "MaxTemperatureC"
    max_temp_day_model = get_max_value_for_year_and_attribute(year, attribute)
    print("\n")
    if max_temp_day_model is not None:
        date_str = max_temp_day_model.__getattribute__("PKT")
        components = datetime.strptime(date_str, "%Y-%m-%d")
        print("Highest:", max_temp_day_model.__getattribute__(attribute) + "C on", components.strftime("%B"),
              str(components.day))

    attribute = "MinTemperatureC"
    min_temp_day_model = get_min_value_for_year_and_attribute(year, attribute)
    if min_temp_day_model is not None:
        date_str = min_temp_day_model.__getattribute__("PKT")
        components = datetime.strptime(date_str, "%Y-%m-%d")
        print("Lowest:", min_temp_day_model.__getattribute__(attribute) + "C on", components.strftime("%B"),
              str(components.day))

    attribute = "MaxHumidity"
    max_humid_day_model = get_min_value_for_year_and_attribute(year, attribute)
    if max_humid_day_model is not None:
        date_str = max_humid_day_model.__getattribute__("PKT")
        components = datetime.strptime(date_str, "%Y-%m-%d")
        print("Humidity:", max_humid_day_model.__getattribute__(attribute) + "% on", components.strftime("%B"),
              str(components.day))


def get_file_names_for_year(year):
    file_prefix_for_year = "Murree_weather_" + year
    file_names_for_year = []
    for file in os.listdir("weatherfiles/"):
        if file.startswith(file_prefix_for_year):
            file_names_for_year.append(file)
    return file_names_for_year


def get_max_value_for_year_and_attribute(year, attribute):
    file_names_for_year = get_file_names_for_year(year)
    max_value = None
    max_in_every_month = []
    for file_name in file_names_for_year:
        month_model = MonthWeatherModel(file_name)
        value_in_string = month_model.find_max_for_attribute(attribute)
        max_in_every_month.append(value_in_string)
    if max_in_every_month.__len__() != 0:
        max_value = max(max_in_every_month, key=operator.attrgetter(attribute))

    return max_value


def get_min_value_for_year_and_attribute(year, attribute):
    file_names_for_year = get_file_names_for_year(year)
    min_value = None
    min_in_every_month = []
    for fileName in file_names_for_year:
        month_model = MonthWeatherModel(fileName)
        value_in_string = month_model.find_min_for_attribute(attribute)
        min_in_every_month.append(value_in_string)
    if min_in_every_month.__len__() != 0:
        min_value = min(min_in_every_month, key=operator.attrgetter(attribute))

    return min_value
