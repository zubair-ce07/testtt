import os
import sys
import argparse
import calendar
from Weather import *

def generate_yearly_filename(year,directory):
    filenames = [directory+'/Murree_weather_'+year+'_'+calendar.month_abbr[int(months_count)]+ \
                '.txt' for months_count in range(12)]
    return filenames

def generate_monthly_filename(date,directory):
    weather_date = date.split("/")
    filename = directory+'/Murree_weather_'+weather_date[0]+'_'+calendar.month_abbr[int(weather_date[1])]+'.txt'
    return filename

def error_message_exit(input=True,record=True):
    if not input:
        print('Invalid Input')
    elif not record:
        print('No record found....')
    sys.exit()

def get_yearly_weather(date,directory):
    weather_date = date.split('/')
    filenames = generate_yearly_filename(weather_date[0],directory)
    yearly_weather = YearlyWeather(filenames)

    if yearly_weather.read_yearly_weather():
        print (yearly_weather)
    else:
        error_message_exit(True,False)

def get_monthly_weather(date,directory):
    monthly_weather = MonthlyWeather(generate_monthly_filename(date,directory))

    if monthly_weather.read_monthly_weather():
        print (monthly_weather)
    else:
        error_message_exit(True,False)

def get_monthly_graphed_weather(date,directory):
    monthly_weather = MonthlyWeather(generate_monthly_filename(date,directory))

    if monthly_weather.read_monthly_weather():
        monthly_weather.read_daily_weather()
    else:
        error_message_exit(True,False)

def get_day_wise_graphed_weather(date,directory):
    monthly_weather = MonthlyWeather(generate_monthly_filename(date,directory))

    if monthly_weather.read_monthly_weather():
         monthly_weather.analyze_daily_graph_weather()
    else:
         error_message_exit(True,False)

def validate_date (date):
    weather_date = date.split('/')

    if len(weather_date) <= 1:
        error_message_exit(False)
    elif int(weather_date[1]) > 12 or int(weather_date[1]) < 0:
        error_message_exit(False)
    else:
        return True

def main ():
    os.system('clear')
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    parser.add_argument('-e')
    parser.add_argument('-a')
    parser.add_argument('-c')
    parser.add_argument('-g')
    args = parser.parse_args()

    if args.a is not None:
        if validate_date(args.a):
            get_monthly_weather (args.a,args.directory)
    if args.e is not None:
        get_yearly_weather (args.e,args.directory)
    if args.c is not None:
        get_monthly_graphed_weather (args.c,args.directory)
    if args.g is not None:
        get_day_wise_graphed_weather (args.g,args.directory)

if __name__== "__main__":
    main()
