import argparse
import calendar
from datetime import datetime

from data_reader import DataReader
from reports_calculator import ReportsCalculator
from reports_generator import ReportsGenerator


def year_validator(year):
    try:
        return datetime.strptime(year, '%Y').strftime('%Y')
    except ValueError:
        print('Please enter a valid year, like 2012')


def date_validator(date):
    try:
        return datetime.strptime(date, '%Y/%m').strftime('%Y/%m')
    except ValueError:
        print('Please enter a valid year and month, like 2015/6')


def date_parser(year_month):
    date = year_month.split('/')
    year, month = date[0], date[1]
    month_name = calendar.month_abbr[int(month)]

    return {'year': year, 'month': month_name}


def main():
    parser = argparse.ArgumentParser(description='Weatherman app')
    parser.add_argument('path')
    parser.add_argument('-e')
    parser.add_argument('-a')
    parser.add_argument('-c')
    args = parser.parse_args()

    weather_reader = DataReader()

    if args.e:
        year = year_validator(args.e)
        if year:
            file_names_e = DataReader.yearly_file_names(args.path, year)

            if file_names_e:
                data = weather_reader.read_files(file_names_e)
                extremes = ReportsCalculator.extreme_values(data)
                ReportsGenerator.display_extrems(extremes)
            else:
                print('No file found for given year')

    elif args.a:
        year_month = date_validator(args.a)
        if year_month:
            date = date_parser(year_month)
            file_names_a = DataReader.monthly_file_names(args.path, date['year'], date['month'])

            if file_names_a:
                data = weather_reader.read_files(file_names_a)
                avg_values = ReportsCalculator.average_values(data)
                ReportsGenerator.display_averages(avg_values)
            else:
                print('No file found for given year and month')

    elif args.c:
        year_month = date_validator(args.c)

        if year_month:
            date = date_parser(year_month)
            file_names_c = DataReader.monthly_file_names(args.path, date['year'], date['month'])
            if file_names_c:
                data = weather_reader.read_files(file_names_c)
                ReportsGenerator.bonus_chart(data)
            else:
                print('No file found for given year and month')


if __name__ == '__main__':
    main()
