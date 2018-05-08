import os
import sys, getopt
import argparse
import calendar
from weather import *

def generate_file_names(year):
    filenames = []

    for months_count in range(12):
        filenames.append('weatherfiles/Murree_weather_'+year+'_'+calendar.month_abbr[int(months_count)]+'.txt')

    return filenames

def get_yearly_weather(date):
    weather_date = date.split('/')
    filenames = generate_file_names(weather_date[0])
    yearly_weather = YearlyWeather(filenames)

    if yearly_weather.verify_yearly_weather():
        yearly_weather_details = yearly_weather.read_yearly_weather()
        print (yearly_weather)
    else:
        print ('No record found against this year')
        sys.exit()

def get_monthly_weather(date):
    weather_date = date.split("/")
    filename = 'weatherfiles/Murree_weather_'+weather_date[0]+'_'+calendar.month_abbr[int(weather_date[1])]+'.txt'
    monthly_weather = MonthlyWeather(filename)

    if monthly_weather.verify_monthly_weather():
        monthly_weather_details = monthly_weather.read_monthly_weather()
        print (monthly_weather)
    else:
        print ('No record found against this month')
        sys.exit()

def get_monthly_graphed_weather(date):
    weather_date = date.split('/')
    filename = 'weatherfiles/Murree_weather_'+weather_date[0]+'_'+calendar.month_abbr[int(weather_date[1])]+'.txt'
    monthly_weather = MonthlyWeather(filename)
    if monthly_weather.verify_monthly_weather():
        monthly_weather.read_daily_weather()
    else:
        print ('No record found against this month')
        sys.exit()

def get_day_wise_graphed_weather(date):
    weather_date = date.split('/')
    filename = 'weatherfiles/Murree_weather_'+weather_date[0]+'_'+calendar.month_abbr[int(weather_date[1])]+'.txt'
    monthly_weather = MonthlyWeather(filename)

    if monthly_weather.verify_monthly_weather():
         monthly_weather.analyze_daily_graph_weather()
    else:
         print ('No record found against this month')
         sys.exit()

def validate_date (date):
    weather_date = date.split('/')

    if len(weather_date) <= 1:
        print('Invalid Input')
        sys.exit()
    elif int(weather_date[1]) > 12 or int(weather_date[1]) < 0:
        print('Invalid Input')
        sys.exit()
    else:
        return True

def main (args):
    os.system('clear')
    date = sys.argv[len(sys.argv)-1]
    yearly_weather = '-e'
    monthly_weather = '-a'
    monthly_weather_with_graph = '-c'
    monthly_weather_with_merged_graph = '-g'

    if args.a is not None:
        if validate_date(args.a):
            get_monthly_weather (args.a)
    if args.e is not None:
        get_yearly_weather (args.e)
    if args.c is not None:
        get_monthly_graphed_weather (args.c)
    if args.g is not None:
        get_day_wise_graphed_weather (args.g)

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e')
    parser.add_argument('-a')
    parser.add_argument('-c')
    parser.add_argument('-g')
    args = parser.parse_args()
    main(args)
