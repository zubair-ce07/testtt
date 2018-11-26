from reader import ReadWeatherData
from calculations import CalculateResults
from report import Reports
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

    args = parser.parse_args()
    path = args.path
    weather = ReadWeatherData(path)
    cal = CalculateResults()
    rep = Reports()

    if args.e:
        year = args.e
        month = None
        weather.read_data_year(str(year))
        result = cal.yearly_result(weather.read_data())
        rep.highest_temp(result)
        rep.lowest_temp(result)
        rep.most_humidty(result)

    elif args.a:
        year_month = datetime.strptime(args.a, '%Y/%m')
        year = year_month.strftime('%Y')
        month = year_month.strftime('%b')
        weather.read_data_file_month(year, month)
        result = cal.average_result(weather.read_data())
        rep.monthly_weather(result)

    elif args.c:
        year_month = datetime.strptime(args.c, '%Y/%m')
        year = year_month.strftime('%Y')
        month = year_month.strftime('%b')
        weather.read_data_file_month(year, month)
        result = cal.monthly_graph(weather.read_data())
        rep.max_min_bar(month, year, result)

    else:
        print("Please select correct option")


if __name__ == '__main__':
    main()
