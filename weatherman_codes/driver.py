"""
Driver file for weatherman
Pylint Score: 10.00
"""

import argparse
from weatherclass import WeatherClass


def main():
    """Main function"""
    weather = WeatherClass()

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

    if args.year:
        # For input -e
        weather.peak_days(args)

    if args.year_month:
        # For input -a
        if args.year_month.find('/') == 4:
            weather.calculate_averages(args)
        else:
            print('Input format should be year/month')

    if args.year_month_graph:
        # For input -c
        weather.make_graph(args)


if __name__ == '__main__':
    main()
