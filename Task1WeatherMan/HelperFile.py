import calendar
import os
from datetime import datetime
from pathlib import Path


WEATHER_FILE_PREFIX = "Murree_weather_"
WEATHER_FOLDER_NAME = "weatherfiles/"


def does_weather_file_exist(file_name):
    file_path = "weatherfiles/" + file_name
    weather_file = Path(file_path)
    return weather_file.is_file()


def get_date_components(input_string):
    try:
        components = datetime.strptime(input_string, '%Y' + '/' + '%m')
    except ValueError:
        return None
    return components


def validate_year_month_input(input_string):
    components = get_date_components(input_string)
    if components:
        file_name = WEATHER_FILE_PREFIX + str(components.year) + "_" + calendar.month_abbr[components.month] + ".txt"
        if does_weather_file_exist(file_name):
            return file_name
    print("\nData for", input_string, "is not available")
    return None


def validate_year_input(input_string):
    components = get_date_components(input_string)
    if components:
        file_name = WEATHER_FILE_PREFIX + str(components.year) + "_" + calendar.month_abbr[components.month] + ".txt"
        if does_weather_file_exist(file_name):
            return file_name
    print("\nData for", input_string, "is not available")
    return None


def get_file_names_for_year(year):
    file_prefix_for_year = WEATHER_FILE_PREFIX + year
    file_names_for_year = []
    for file in os.listdir(WEATHER_FOLDER_NAME):
        if file.startswith(file_prefix_for_year):
            file_names_for_year.append(file)
    return file_names_for_year
