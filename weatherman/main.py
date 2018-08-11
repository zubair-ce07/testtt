import re
import sys


def validate_input(args):
    if len(args) is not 4:
        return False
    if not re.match(r'-[eac]$', args[1]):
        return False
    if args[1][1] is 'e':
        if not re.match(r'\d{4}$', args[2]):
            return False
    else:
        if not re.match(r'\d{4}/((0?[1-9])|(1[012]))$', args[2]):
            return False
    return True


def main():
    print("{} {}".format(len(sys.argv), validate_input(sys.argv)))


main()
