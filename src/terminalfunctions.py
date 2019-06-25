import re
import os

def validate_arguments(args):
    size = len(args)
    if size % 2 != 0:
        print("Wrong usage!")
        return False
    if size < 4:
        print("Not enough arguments")
        return False
    if not os.path.exists(args[1]):
        print("Invalid path")
        return False
    for i in range(2, size - 1, 2):
        args[i]= str(args[i])
        if args[i] != '-e' and args[i] != '-a' and args[i] != '-c' and args[i] != '-b':
            print(f"Invalid flag entered: {args[i]}")
            return False
        value_passed = args[i+1]
        if args[i] == "-a" or args[i] == "-c" or args[i] == "-b":
            if not re.match("\\d{4}/\\d{2}", str(value_passed)) and not re.match("\\d{4}/\\d{1}", str(value_passed)):
                print("Wrong usage!")
                return False
    return True

def print_usage():
    print("Usage: weatherman.py path/to/files-dir [-e YYYY] [-a YYYY/MM] [-c YYYY/MM] [-b YYYY/MM]")
