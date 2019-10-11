from constants import COLORS


def int_divison_util(total, count):
    try:
        result = total // count
    except ZeroDivisionError:
        result = 'Unavailable'

    return result


def colored_string(string, color, times=1):
    return f"{color}{string*int(times)}{COLORS['RESET']}"


def is_valid_int(val):
    try:
        int(val)
        return True
    except ValueError:
        pass
    except TypeError:
        pass

    return False
