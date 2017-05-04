import operator

import helperfile
from monthweather import MonthWeatherModel
from datetime import datetime


def highest_lowest_temperature_and_humidity(year):
    max_temp_day_model = get_max_value_for_year_and_attribute(year, "max_temperature")
    print("\n")
    if max_temp_day_model:
        date_str = max_temp_day_model.date
        components = datetime.strptime(date_str, "%Y-%m-%d")
        print("Highest:", max_temp_day_model.max_temperature + "C on", components.strftime("%B"),
              str(components.day))

    min_temp_day_model = get_min_value_for_year_and_attribute(year, "min_temperature")
    if min_temp_day_model is not None:
        date_str = min_temp_day_model.date
        components = datetime.strptime(date_str, "%Y-%m-%d")
        print("Lowest:", min_temp_day_model.min_temperature + "C on", components.strftime("%B"),
              str(components.day))

    max_humid_day_model = get_min_value_for_year_and_attribute(year, "max_humidity")
    if max_humid_day_model is not None:
        date_str = max_humid_day_model.date
        components = datetime.strptime(date_str, "%Y-%m-%d")
        print("Humidity:", max_humid_day_model.max_humidity + "% on", components.strftime("%B"),
              str(components.day))


def get_max_value_for_year_and_attribute(year, attribute):
    file_names_for_year = helperfile.get_file_names_for_year(year)
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
    file_names_for_year = helperfile.get_file_names_for_year(year)
    min_value = None
    min_in_every_month = []
    for fileName in file_names_for_year:
        month_model = MonthWeatherModel(fileName)
        value_in_string = month_model.find_min_for_attribute(attribute)
        min_in_every_month.append(value_in_string)
    if min_in_every_month.__len__() != 0:
        min_value = min(min_in_every_month, key=operator.attrgetter(attribute))

    return min_value
