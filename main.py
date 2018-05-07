import os
import sys, getopt
import argparse
from weather import *

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def clear_screen():
    os.system('clear')

def get_month_name(num_of_month):
    if int(num_of_month) > 12 or int(num_of_month) < 0 :
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        main()
    else:
        return months[int(num_of_month)-1]

def generate_file_names(year):
    filenames = []

    for months_count in months:
        filenames.append('weatherfiles/Murree_weather_'+year+'_'+months_count+'.txt')

    return filenames

def get_formatted_date(date):
    segmented_date = date.split('-')
    formatted_date = months[int(segmented_date[1])-1]+' '+segmented_date[2]
    return formatted_date

def get_yearly_data(user_input,index):
    try:
        user_provided_year = user_input[index].split('/')
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        main()
    finally:
        if len(user_provided_year) > 1 :
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            main()
        else:
             filenames = generate_file_names(user_provided_year[0])
             yearly_weather = YearlyWeather(filenames)
             if yearly_weather.verify_yearly_data():
                 yearly_weather_details = yearly_weather.get_yearly_weather()
                 print ('Highest Temperature: %sC on %s'%(yearly_weather_details['highest_annual_temperature'],get_formatted_date(yearly_weather_details['highest_annual_temperature_date'])))
                 print ('Lowest Temperature: %sC on %s'%(yearly_weather_details['lowest_annual_temperature'],get_formatted_date(yearly_weather_details['lowest_annual_temperature_date'])))
                 print ('Highest Humidity: %s%% on %s'%(yearly_weather_details['highest_annual_humidity'],get_formatted_date(yearly_weather_details['highest_annual_humidity_date'])))
             else:
                 print ('No record found against this year')
                 keypress = input('Press any key to continue...')
                 main()

def get_monthly_data (user_input,index):
    try:
        user_provided_year_month = user_input[index].split('/')
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        main()
    finally:
        if len(user_provided_year_month) == 1 or len(user_provided_year_month) == 0 :
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            main()
        else:
             month = get_month_name(int(user_provided_year_month[1]))
             if month != -1:
                 filename = 'weatherfiles/Murree_weather_'+user_provided_year_month[0]+'_'+month+'.txt'
                 monthly_weather = MonthlyWeather(filename)
                 if monthly_weather.verify_monthly_data():
                     monthly_weather_details = monthly_weather.get_monthly_weather()
                     print('Highest Average: %sC'%(monthly_weather_details['monthly_highest_average']))
                     print('Lowest Average: %sC'%(monthly_weather_details['monthly_lowest_average']))
                     print('Average Mean Humidity: %s%%'%(monthly_weather_details['monthly_average_mean_humidity']))
                 else:
                     print ('No record found against this month')
                     keypress = input('Press any key to continue...')
                     main()

def get_monthly_graphed_data (user_input,index):
    try:
        user_provided_year_month = user_input[index].split('/')
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        main()
    finally:
        if len(user_provided_year_month) == 1 or len(user_provided_year_month) == 0:
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            main()
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
                     main()

def get_day_wise_graphed_data (user_input,index):
    try:
        user_provided_year_month = user_input[index].split('/')
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        main()
    finally:
        if len(user_provided_year_month) == 1 or len(user_provided_year_month) == 0:
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            main()
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
                     main()

def main (argv):
    clear_screen()
    date = sys.argv[len(sys.argv)-1]
    yearly_data = '-e'
    monthly_data = '-a'
    monthly_data_with_graph = '-c'
    monthly_data_with_merged_graph = '-g'

    for index,val in enumerate(sys.argv):
        if yearly_data in val:
            get_yearly_data (sys.argv,index+1)
        if monthly_data in val:
            get_monthly_data (sys.argv,index+1)
        if monthly_data_with_graph in val:
            get_monthly_graphed_data (sys.argv,index+1)
        if monthly_data_with_merged_graph in val:
            get_day_wise_graphed_data (sys.argv,index+1)

if __name__== "__main__":
    main(sys.argv[1:])
