import argparse
from datetime import datetime

from weather_files_reader import *
from reports_calculator import *
from reports_generator import *


def extract_year_records(weather_records, date):           
    return [record for record in weather_records if date.year == record.record_date.year]        


def extract_month_records(weather_records, date):   
    return [record for record in weather_records if date.year == record.record_date.year
            and date.month == record.record_date.month]  


def main():
    parser = argparse.ArgumentParser(description='Weatherman app')
    parser.add_argument('path')
    parser.add_argument('-e', type=lambda year: datetime.strptime(year, '%Y'), nargs='?')
    parser.add_argument('-a', type=lambda date: datetime.strptime(date, '%Y/%m'), nargs='?')
    parser.add_argument('-c', type=lambda date: datetime.strptime(date, '%Y/%m'), nargs='?')
    args = parser.parse_args()
    
    weather_records = read_weather_files(args.path)

    if args.e:
        year_records = extract_year_records(weather_records, args.e)                 
        yearly_report = calculate_yearly_report(year_records)
        display_yearly_report(yearly_report)
              
    if args.a:
        month_records = extract_month_records(weather_records, args.a)                                                       
        monthly_report = calculate_monthly_report(month_records)
        display_monthly_report(monthly_report) 
       
    if args.c:                               
        month_records = extract_month_records(weather_records, args.a)        
        display_month_bar_chart(month_records)                             
       
if __name__ == '__main__':
    main()
    