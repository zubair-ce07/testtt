import os
import glob  # allows pattern matching on file_names
import datetime


# validate_year takes the value and validate for year
def validate_year(year):
    """
    :param year:
    :return:
    """
    try:
        if year:
            if year.isdigit():
                year = int(year)
                current_year = datetime.datetime.now().year
                if 1900 <= year <= current_year:
                    return year
                else:
                    return False
            else:
                return False
        else:
            return None
    except ValueError:
        return "Format Error"


# validate_year takes the value and validate for year
def validate_year_and_month(year_month):
    """
    :param year_month:
    :return:
    """
    try:
        if year_month:
            year = year_month.split('/')[0]
            is_year_valid= validate_year(year)
            if is_year_valid:
                month = year_month.split('/')[1]
                if month.isdigit():
                    month = int(month)
                    if 1 <= month <= 12:
                        return year_month
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return None
    except ValueError:
        return "Format Error"


def validate_path(path):
    """
    :param path:
    :return:
    """
    if path:
        is_directory_exist= os.path.isdir(path)
        if is_directory_exist:
            return path
        else:
            return False
    else:
        return None


def verify_year_month_weather_readings_exist_and_read_file_paths(path,year,month="*"):
    """
    :param path:
    :param year:
    :param month:
    :return:
    """
    file_paths = []
    file_path = path + "/Murree_weather_" + str(year) + "_" + month + ".txt"
    for f_path in glob.glob(file_path):
        file_paths.append(f_path)
    return file_paths

