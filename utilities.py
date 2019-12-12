import datetime


def round_float(float_number):
    """Rounds float numbers to 2 decimal places"""
    return format(float_number, '.2f')


def parse_date(date, date_format):
    """Returns date in format given by user"""
    return datetime.datetime.strptime(date, date_format)


def change_color(color):
    """Returns to sequence to change the color of text in console to the given color"""
    return f'\033[0;{color};40m'


def reset_color():
    """Returns to sequence to reset the color of text in console """
    return f'\033[0;0m'


def draw_bar_graph(day, upper_limit, lower_limit, upper_limit_color, lower_limit_color, unit):
    """Returns a combined bar graph with lower and upper limits which can be used in stdout and other streams"""
    return f'{day} {generate_graph(lower_limit, lower_limit_color)}{generate_graph(upper_limit, upper_limit_color)} '\
           f'{reset_color()}{lower_limit}{unit} - {upper_limit}{unit}'


def generate_graph(points, color):
    """Returns bar graphs according to the color and value"""
    return f"{change_color(color)}{points * '+'}"


def format_date(date):
    """Returns date in format of Month, Year e.g. November, 2016"""
    return f"{datetime.datetime.strftime(date, '%B, %Y')}"


def str_to_float(str_value):
    """takes string number, convert it to float and return it, if string is empty then it returns 0.0"""
    try:
        return float(str_value)
    except ValueError:
        return 0.0
