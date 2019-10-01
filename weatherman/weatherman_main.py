import argparse
from datetime import datetime

from weather_files_reader import *
from reports_calculator import *
from reports_generator import *
import error_messages


def find_month_data(weather_data, date):
    monthly_weather_data = []
    month_year = date.strftime('%Y-%m')

    for monthly_weather_record in weather_data:
        if month_year in monthly_weather_record.weather_record_date.strftime('%Y-%m'):
            monthly_weather_data.append(monthly_weather_record)

    return monthly_weather_data

def find_year_data(weather_data, year):
    yearly_weather_data = []

    for yearly_weather_record in weather_data:
        if year in yearly_weather_record.weather_record_date.strftime('%Y'):
            yearly_weather_data.append(yearly_weather_record)

    return yearly_weather_data 

def main():
    parser = argparse.ArgumentParser(description='Weatherman app')
    parser.add_argument('path')
    parser.add_argument('-e', type=lambda year: datetime.strptime(year, '%Y'), nargs='?')
    parser.add_argument('-a', type=lambda date: datetime.strptime(date, '%Y/%m'), nargs='?')
    parser.add_argument('-c', type=lambda date: datetime.strptime(date, '%Y/%m'), nargs='?')
    args = parser.parse_args()
    
    weather_data = read_weather_files(args.path)

    if args.e:
        year = args.e.strftime('%Y')
        yearly_weather_data = find_year_data(weather_data, year)

        if yearly_weather_data:
            min_and_max_values = calculate_yearly_report(yearly_weather_data)
            display_yearly_report(min_and_max_values)
        else:
            print(error_messages.YEAR_DATA_NOT_FOUND_ERROR)        

    if args.a:
        monthly_weather_data = find_month_data(weather_data, args.a)

        if monthly_weather_data:                                           
            weather_average_values = calculate_monthly_report(monthly_weather_data)
            display_monthly_report(weather_average_values) 
        else:
            print(error_messages.MONTH_DATA_NOT_FOUND_ERROR)                           
       
    if args.c:
        monthly_weather_data = find_month_data(weather_data, args.c)

        if monthly_weather_data:                        
            chart_values = calculate_monthly_chart_values(monthly_weather_data)
            display_month_bar_chart(chart_values)
        else:
            print(error_messages.MONTH_DATA_NOT_FOUND_ERROR)                           
       
if __name__ == '__main__':
    main()
    