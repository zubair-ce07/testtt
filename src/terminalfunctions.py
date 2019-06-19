import re

def validateArguments(args):
    size = len(args)
    if (size%2 != 0):
        print("Size not even")
        return False
    if (size < 4):
        print("Size less than 4")
        return False
    for i in range(2, size-1, 2):
        args[i]= str(args[i])
        if (args[i] != '-e' and args[i] != '-a' and args[i] != '-c'):
            print("Flags not in place")
            print("wrong value of flag:", args[i])
            print("Iteration num:", i)
            return False
        value_passed = args[i+1]
        if (args[i] == "-e"):
            year = int(value_passed)
            if (year < 2004 or year > 2016):
                print("Out of bound year with e")
                return False
        if (args[i] == "-a" or args[i] == "-c"):
            data = str(value_passed)
            if (re.match("\\d{4}/\\d{2}", data) != None or re.match("\\d{4}/\\d{1}", data) != None):
                combined = data.split('/')
                split_year = int(combined[0])
                split_month = int(combined[1])
                if (split_year < 2004 or split_year > 2016):
                    print("Out of bound year with a/c")
                    return False
                if (split_month < 1 or split_month > 12):
                    print("Out of bound month with a/c")
                    return False
            else:
                print("Format not followed with a/c")
                return False
    return True

def printUsage():
    print("Wrong usage!")
    print("Usage: weatherman.py path/to/files-dir [-e YYYY] [-a YYYY/MM] [-c YYYY/MM]")
