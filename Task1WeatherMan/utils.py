import calendar
import os
from pathlib import Path

WEATHER_FILE_PREFIX = "Murree_weather_"
WEATHER_FOLDER_NAME = ""


def file_exists(file_name):
    file_path = WEATHER_FOLDER_NAME + file_name
    weather_file = Path(file_path)
    return weather_file.is_file()


def get_file_name(date):
    file_name = WEATHER_FILE_PREFIX + str(date.year) + "_" + calendar.month_abbr[date.month] + ".txt"
    if file_exists(file_name):
        return file_name


def get_year_files(year):
    files_prefix = WEATHER_FILE_PREFIX + str(year)
    file_names = []
    for file in os.listdir(WEATHER_FOLDER_NAME):
        if file.startswith(files_prefix):
            file_names.append(file)
    return file_names
