import argparse
import calendar
from datetime import datetime

import error_messages
import reports_generator
from weather_files_reader import WeatherDataReader
from reports_calculator import ReportsCalculator


def parse_date(year_month):
    year = datetime.strptime(year_month, '%Y/%m').strftime('%Y')
    month = datetime.strptime(year_month, '%Y/%m').strftime('%m')
    month_name = calendar.month_abbr[int(month)]

    return {'year': year, 'month': month_name}


def main():
    parser = argparse.ArgumentParser(description='Weatherman app')
    parser.add_argument('path')
    parser.add_argument('-e', type=lambda year: datetime.strptime(year, '%Y').strftime('%Y'), nargs='+')
    parser.add_argument('-a', type=lambda date: datetime.strptime(date, '%Y/%m').strftime('%Y/%m'), nargs='+')
    parser.add_argument('-c', type=lambda date: datetime.strptime(date, '%Y/%m').strftime('%Y/%m'), nargs='+')
    args = parser.parse_args()

    weather_reader = WeatherDataReader()
    reports_calculator = ReportsCalculator()

    if args.e:
        file_names_e = WeatherDataReader.read_yearly_file_names(args.path, args.e[0])

        if file_names_e:
            weather_data = weather_reader.read_files(file_names_e)
            min_and_max_values = reports_calculator.calculate_min_max(weather_data)
            reports_generator.display_yearly_report(min_and_max_values)     
        else:
            print(error_messages.YEAR_FILE_NOT_FOUND_ERROR)                

    if args.a:        
        date = parse_date(args.a[0])
        file_names_a = WeatherDataReader.read_monthly_file_names(args.path, date)

        if file_names_a:
            weather_data = weather_reader.read_files(file_names_a)
            avg_values = reports_calculator.calculate_averages(weather_data)
            reports_generator.display_averages(avg_values)                            
        else:
            print(error_messages.MONTH_FILE_NOT_FOUND_ERROR)

    if args.c:        
        date = parse_date(args.c[0])
        file_names_c = WeatherDataReader.read_monthly_file_names(args.path, date)

        if file_names_c:
            weather_data = weather_reader.read_files(file_names_c)
            reports_generator.display_month_bar_chart(weather_data)                           
        else:
            print(error_messages.MONTH_FILE_NOT_FOUND_ERROR)


if __name__ == '__main__':
    main()
    