"""
Driver file for weatherman
Pylint Score: 10.00
"""

import argparse
from weatherman_helpers import get_files, read_data, show_peak_days, show_averages, make_graph


def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--year_month_graph', type=str,
                        help='Show bar graph of a month. Input format: year/month')
    parser.add_argument('-a', '--year_month', type=str,
                        help='Show average max, min temperature & humidity of the month. '
                             'Input format: year/month')
    parser.add_argument('-e', '--year', type=str,
                        help='Show highest & lowest temperatures & mean humidity of the year. '
                             'Input format: year')
    parser.add_argument('directory', type=str, help='files directory path')

    args = parser.parse_args()

    files = get_files(args)

    if files:
        weather_record = read_data(args.directory, files)

        if args.year:               # For input -e
            show_peak_days(args.year, weather_record)

        if args.year_month:         # For input -a
            show_averages(args.year_month, weather_record)

        if args.year_month_graph:   # For input -c
            make_graph(args.year_month_graph, weather_record)

    else:
        print('No files found against your input.')
        print('For -e, Input range: 1996 - 2011')
        print('For -a and -c, Input range: 1996/12 - 2011/12')


if __name__ == '__main__':
    main()
