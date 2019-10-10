import sys

from constants import COLORS

def calculate_avg(total, count):
    try:
        result = total // count
    except ZeroDivisionError:
        result = 'Unavailable'

    return result

def file_handle(file_path):
    try:
        file = open(file_path, 'r')
    except IOError:
        print("Could not read file:", file_path)
        sys.exit()

    return file

def colored_string(str, color, times = 1):
    return f"{color}{str*int(times)}{COLORS['RESET']}"

def check_blank_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    if (line.strip()):
        return False
    else:
        return True
