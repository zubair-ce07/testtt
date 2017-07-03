import sys
from optparse import OptionParser
from weather_record import WeatherRecord


def get_input():
    # Checking whether command line arguments are given or not
    if len(sys.argv) == 1 or len(sys.argv) > 4:
        print("Compile program as : weather_man.py -a -e -c"
              " date /path/to/files")
        sys.exit(2)

    parser = OptionParser()
    parser.add_option("-a", dest="average", action='store_true', default=False)
    parser.add_option("-e", dest="extreme", action='store_true')
    parser.add_option("-c", dest="chart", action='store_true')

    (options, args) = parser.parse_args()

    option = None

    if options.average:
        option = 'a'
    elif options.extreme:
        option = 'e'
    elif options.chart:
        option = 'c'

    return option, args[0], args[1]


if __name__ == "__main__":
    option, date, path_to_files = get_input()
    weather_record = WeatherRecord(path_to_files)

    if option == 'a':
        weather_record.print_average_weather_report(date)
    elif option == 'e':
        weather_record.print_extreme_weather_report(date)
    elif option == 'c':
        weather_record.print_monthly_report(date)
