import os
import sys

from weatherman import WeatherReport


def parse_arguments(argv):
    if len(argv) > 3 and len(argv) % 2 == 0:
        path = argv[1]
        opts = {}  # Empty dictionary to store actions to perform.
        while argv:  # While there are arguments left to parse.
            if argv[0][0] == '-':  # Found a "-name value" pair.
                opts[argv[0]] = argv[1]
            argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
        return opts, path.split('-')[0]
    else:
        return None, None


def main():
    location = 'Murree'
    my_argv, path = parse_arguments(sys.argv)
    if my_argv and path:
        try:
            os.system("ls " + path + " > files_names")
            if '-e' in my_argv:
                WeatherReport().get_yearly_insights(my_argv['-e'], path)
            if '-a' in my_argv:
                WeatherReport().get_monthly_insights(my_argv['-a'], path, location)
            if '-c' in my_argv:
                WeatherReport().get_days_insights(my_argv['-c'], path, location)

        except FileNotFoundError:
            print('Files path is incorrect')
    else:
        print("usage: weatherman.py /path/to/files-dir [option] [year/month] \n"
              "Options:\n-e\tYearly Report\n-a\tMonthly Report\n-c\tDaily Report")


if __name__ == "__main__":
    main()
