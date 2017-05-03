from pathlib import Path


def does_weather_file_exist(file_name):
    file_path = "weatherfiles/" + file_name
    weather_file = Path(file_path)
    if weather_file.is_file():
        return True
    else:
        return False


def get_month_abbreviation(month_num):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if month_num >= 1 and month_num <= 12:
        return months[month_num-1]
    else:
        return ''
