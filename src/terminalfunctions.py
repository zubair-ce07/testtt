import re

def validate_arguments(args):
    size = len(args)
    if size % 2 != 0:
        return False
    if size < 4:
        return False
    for i in range(2, size - 1, 2):
        args[i]= str(args[i])
        if args[i] != '-e' and args[i] != '-a' and args[i] != '-c' and args[i] != '-b':
            return False
        value_passed = args[i+1]
        if args[i] == "-e":
            year = int(value_passed)
            if year < 2004 or year > 2016:
                return False
        if args[i] == "-a" or args[i] == "-c" or args[i] == "-b":
            data = str(value_passed)
            if re.match("\\d{4}/\\d{2}", data) or re.match("\\d{4}/\\d{1}", data):
                combined = data.split('/')
                split_year = int(combined[0])
                split_month = int(combined[1])
                if split_year < 2004 or split_year > 2016:
                    return False
                if split_month < 1 or split_month > 12:
                    return False
            else:
                return False
    return True

def print_usage():
    print("Wrong usage!")
    print("Usage: weatherman.py path/to/files-dir [-e YYYY] [-a YYYY/MM] [-c YYYY/MM] [-b YYYY/MM]")
