import os
import glob  # allows pattern matching on file_names
import datetime


# validate_year takes the value and validate for year
def validate_date(year=1970, month=1):
    """
    :param year:
    :param month:
    :return:
    """
    try:
        year = int(year)
        datetime.datetime(year=year, month=month, day=1)
        return year
    except:
        return False


# validate_year takes the value and validate for year
def validate_year_and_month(year_month):
    """
    :param year_month:
    :return:
    """
    try:
        year_month_value = year_month.split('/')
        year = validate_date(year_month_value[0],year_month_value[1])
        return year_month
    except:
        return False


def validate_path(path):
    """
    :param path:
    :return:
    """
    is_directory_exist = os.path.isdir(path)
    if is_directory_exist:
        return path
    else:
        return False


def verify_year_month_weather_readings_exist_and_read_file_paths(path, year, month="*"):
    """
    :param path:
    :param year:
    :param month:
    :return:
    """
    file_paths = list()
    file_path = path + "/Murree_weather_" + year + "_" + month + ".txt"
    for file_path_ in glob.glob(file_path):
        file_paths.append(file_path_)
    return file_paths
