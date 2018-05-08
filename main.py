import os
import sys, getopt
import argparse
import calendar
from weather import *

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def clear_screen():
    os.system('clear')

def get_month_name(num_of_month):
    if int(num_of_month) > 12 or int(num_of_month) < 0 :
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        sys.exit()
    else:
        return months[int(num_of_month)-1]

def generate_file_names(year):
    filenames = []

    for months_count in months:
        filenames.append('weatherfiles/Murree_weather_'+year+'_'+months_count+'.txt')

    return filenames

def get_yearly_data(date):
    try:
        user_provided_year = date.split('/')
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        sys.exit()
    finally:
        if len(user_provided_year) > 1 :
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            sys.exit()
        else:
             filenames = generate_file_names(user_provided_year[0])
             yearly_weather = YearlyWeather(filenames)
             if yearly_weather.verify_yearly_data():
                 yearly_weather_details = yearly_weather.get_yearly_weather()
                 print (yearly_weather)
             else:
                 print ('No record found against this year')
                 keypress = input('Press any key to continue...')
                 sys.exit()

def get_monthly_data (date):
    try:
        user_provided_year_month = date.split('/')
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        sys.exit()
    finally:
        if len(user_provided_year_month) == 1 or len(user_provided_year_month) == 0 :
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            sys.exit()
        else:
             month = get_month_name(int(user_provided_year_month[1]))
             if month != -1:
                 filename = 'weatherfiles/Murree_weather_'+user_provided_year_month[0]+'_'+month+'.txt'
                 monthly_weather = MonthlyWeather(filename)
                 option = []
                 if monthly_weather.verify_monthly_data():
                     monthly_weather_details = monthly_weather.get_monthly_weather()
                     print (monthly_weather)
                 else:
                     print ('No record found against this month')
                     keypress = input('Press any key to continue...')
                     sys.exit()

def get_monthly_graphed_data (date):
    try:
        user_provided_year_month = date.split('/')
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        sys.exit()
    finally:
        if len(user_provided_year_month) == 1 or len(user_provided_year_month) == 0:
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            sys.exit()
        else:
             month = get_month_name(int(user_provided_year_month[1]))
             if month != -1:
                 filename = 'weatherfiles/Murree_weather_'+user_provided_year_month[0]+'_'+month+'.txt'
                 monthly_weather = MonthlyWeather(filename)
                 if monthly_weather.verify_monthly_data():
                     monthly_weather.get_daily_temperature()
                 else:
                     print ('No record found against this month')
                     keypress = input('Press any key to continue...')
                     sys.exit()

def get_day_wise_graphed_data (date):
    try:
        user_provided_year_month = date.split('/')
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        sys.exit()
    finally:
        if len(user_provided_year_month) == 1 or len(user_provided_year_month) == 0:
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            sys.exit()
        else:
             month = get_month_name(int(user_provided_year_month[1]))
             if month != -1:
                 filename = 'weatherfiles/Murree_weather_'+user_provided_year_month[0]+'_'+month+'.txt'
                 monthly_weather = MonthlyWeather(filename)

                 if monthly_weather.verify_monthly_data():
                     monthly_weather.read_data_for_daily_graph()
                 else:
                     print ('No record found against this month')
                     keypress = input('Press any key to continue...')
                     sys.exit()

def main (args):
    clear_screen()
    date = sys.argv[len(sys.argv)-1]
    yearly_data = '-e'
    monthly_data = '-a'
    monthly_data_with_graph = '-c'
    monthly_data_with_merged_graph = '-g'

    if args.a is not None:
        get_monthly_data (args.a)
    if args.e is not None:
        get_yearly_data (args.e)
    if args.c is not None:
        get_monthly_graphed_data (args.c)
    if args.g is not None:
        get_day_wise_graphed_data (args.g)

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e')
    parser.add_argument('-a')
    parser.add_argument('-c')
    parser.add_argument('-g')
    args = parser.parse_args()
    main(args)
