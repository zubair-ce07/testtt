import sys
import os
from weatherman.weather_man import WeatherReport


def parse_arguments(argv):
    path = argv[1]
    opts = {}  # Empty dictionary to store actions to perform.
    while argv:  # While there are arguments left to parse.
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts, path.split('-')[0]


def main():
    my_argv, path = parse_arguments(sys.argv)
    os.system("ls " + path + " > files_names")
    if '-e' in my_argv:
        WeatherReport().get_yearly_insights(my_argv['-e'], path)
    if '-a' in my_argv:
        WeatherReport().get_monthly_insights(my_argv['-a'], path)


if __name__ == "__main__":
    main()
