import re
import sys
from datetime import date

YEARLY_HIGHEST_LOWEST_HUMID = 1
AVERAGE_TEMPERATURE = 2
TWO_LINE_CHART = 3
ONE_LINE_CHART = 4


def validate_input(args):
    if len(args) is not 4:
        return False
    if not re.match(r'-[eac]$', args[1]):
        return False
    if args[1][1] is 'e':
        if not re.match(r'\d{4}$', args[2]):
            return False
    else:
        if not re.match(r'^(\d{4})/((0?[1-9])|(1[012]))$', args[2]):
            return False
    return True


def generate_date(year, month=1, day=1):
    return date(int(year), int(month), int(day))


def parse_input(args):
    """Parse the input to decide what to do."""
    operation = None
    weather_date = None
    path_to_files = None

    if args[1] == '-e':
        operation = YEARLY_HIGHEST_LOWEST_HUMID
    elif args[1] == "-a":
        operation = AVERAGE_TEMPERATURE
    elif args[1] == "-c":
        operation = TWO_LINE_CHART
    else:
        operation = ONE_LINE_CHART

    if operation == YEARLY_HIGHEST_LOWEST_HUMID:
        weather_date = generate_date(args[2][:4])
    else:
        weather_date = generate_date(args[2][:4], args[2][5:])

    path_to_files = args[3]

    return operation, weather_date, path_to_files


def main():
    print("{} {}".format(len(sys.argv), validate_input(sys.argv)))
    operation, weather_date, path_to_files = parse_input(sys.argv)


if __name__ == "__main__":
    main()
