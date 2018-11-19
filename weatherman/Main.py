from weatherFunc import Weather
from datetime import datetime
import argparse

"""
This is the main() here we define our command line argurment
for the program and specify all the fucntions to run for a specific
argument
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to Directory', type=str)
    parser.add_argument('-e', help='Required argurment "year"')
    parser.add_argument('-a', help='Required argument "year/month"')
    parser.add_argument('-c', help='Required argument "year/month"')
    parser.add_argument('-d', help='Required argument "year/month"')

    args = parser.parse_args()
    path = args.path
    weather = Weather(path)

    if args.e:
        year = args.e
        month = None
        weather.read_data_year(str(year))
        weather.read_data()
        weather.filter_data()
        weather.hot_cold_humid_day()

    elif args.a:
        year_month = datetime.strptime(args.a, '%Y/%m')
        year = year_month.strftime('%Y')
        month = year_month.strftime('%b')
        weather.read_data_file_month(year, month)
        weather.read_month_data()
        weather.filter_data()
        weather.average_max_min_humid_day()

    elif args.c:
        year_month = datetime.strptime(args.c, '%Y/%m')
        year = year_month.strftime('%Y')
        month = year_month.strftime('%b')
        weather.read_data_file_month(year, month)
        weather.read_month_data()
        weather.filter_data()
        weather.max_min_bar(month, year)

    elif args.d:
        year_month = datetime.strptime(args.d, '%Y/%m')
        year = year_month.strftime('%Y')
        month = year_month.strftime('%b')
        weather.read_data_file_month(year, month)
        weather.read_month_data()
        weather.filter_data()
        weather.one_bar(month, year)
    else:
        print("Please select correct option")

if __name__ == '__main__':
        main()
