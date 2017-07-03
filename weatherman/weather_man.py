import sys
from optparse import OptionParser
from weather_record import WeatherRecord


def get_year(date):
    year = date.split('/')[0]
    return year


def get_month(date):
    split_date = date.split('/')
    if len(split_date) > 1:
        month = int(split_date[1])
        return month
    else:
        print "-----No Relevant Data Found-----"
        print "Month not specified in the input"
        exit(2)


def get_input():
    """Checking whether command line arguments are given or not"""
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

    year = get_year(date)

    if option == 'a':
        month = get_month(date)
        weather_record.print_average_weather_report(year, month)

    elif option == 'e':
        weather_record.print_extreme_weather_report(year)

    elif option == 'c':
        month = get_month(date)
        weather_record.print_monthly_report(year, month)
