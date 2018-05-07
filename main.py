import os
import sys
from weather import *

def clearScreen ():                                             #clears console
    os.system('clear')

def numberToWordsMapperForMonths (num_of_month):                #converts numeric month to words
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if int(num_of_month) > 12 or int(num_of_month) < 0 :
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        _main_()
    else:
        return months[int(num_of_month)-1]

def generateFileNameAccordingToYear (year):                     #creates filename according to year
    months_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    filenames_list = []

    for months_count in months_list:
        filenames_list.append('weatherfiles/Murree_weather_'+year+'_'+months_count+'.txt')

    return filenames_list

def getFormattedDate (date):                                               #converts numeric date into modified form
    months_list = ['January','Feburary','March','April','May','June','July','August','September','Octuber','November','December']
    segmented_date = date.split('-')
    formatted_date = months_list[int(segmented_date[1])-1]+' '+segmented_date[2]
    return formatted_date

def getDataForParticularYear (user_input,index):                #fetches data for particular year with year object
    try:
        user_provided_year = user_input[index].split('/')
        if len(user_provided_year) > 1 :
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            _main_()
        else:
             filenames = generateFileNameAccordingToYear (user_provided_year[0])
             yearly_data = YearlyWeather(filenames)
             if yearly_data.verifyYearlyData():
                 yearly_weather_details = yearly_data.getYearlyValuesForTemperature()
                 print ('Highest Temperature: %sC on %s'%(yearly_weather_details['highest_annual_temperature'],getFormattedDate(yearly_weather_details['highest_annual_temperature_date'])))
                 print ('Lowest Temperature: %sC on %s'%(yearly_weather_details['lowest_annual_temperature'],getFormattedDate(yearly_weather_details['lowest_annual_temperature_date'])))
                 print ('Highest Humidity: %s%% on %s'%(yearly_weather_details['highest_annual_humidity'],getFormattedDate(yearly_weather_details['highest_annual_humidity_date'])))
                 sys.exit()
             else:
                 print ('No record found against this year')
                 keypress = input('Press any key to continue...')
                 _main_()
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        _main_()

def getDataForParticularMonth (user_input,index):               #fetches data for particular month with month object
    try:
        user_provided_year_month = user_input[index].split('/')
        if len(user_provided_year_month) == 1 or len(user_provided_year_month) == 0 :
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            _main_()
        else:
             month = numberToWordsMapperForMonths (int(user_provided_year_month[1]))
             if month != -1:
                 filename = 'weatherfiles/Murree_weather_'+user_provided_year_month[0]+'_'+month+'.txt'
                 monthly_data = MonthlyWeather(filename)
                 if monthly_data.verifyDataForMonth():
                     monthly_weather_details = monthly_data.getDataForMonth();
                     print('Highest Average: %sC'%(monthly_weather_details['monthly_highest_average']))
                     print('Lowest Average: %sC'%(monthly_weather_details['monthly_lowest_average']))
                     print('Average Mean Humidity: %s%%'%(monthly_weather_details['monthly_average_mean_humidity']))
                     sys.exit()
                 else:
                     print ('No record found against this month')
                     keypress = input('Press any key to continue...')
                     _main_()
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        _main_()

def getDataInGraphForCompleteMonth (user_input,index):          #fetches monthly data in form of graph
    try:
        user_provided_year_month = user_input[index].split('/')
        if len(user_provided_year_month) == 1 or len(user_provided_year_month) == 0:
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            _main_()
        else:
             month = numberToWordsMapperForMonths (int(user_provided_year_month[1]))
             if month != -1:
                 filename = 'weatherfiles/Murree_weather_'+user_provided_year_month[0]+'_'+month+'.txt'
                 monthly_data = MonthlyWeather(filename)

                 if monthly_data.verifyDataForMonth():
                     monthly_data.readMaxAndMinTemperaturePerDay()
                     sys.exit();
                 else:
                     print ('No record found against this month')
                     keypress = input('Press any key to continue...')
                     _main_()
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        _main_()

def getDailyGraphReportForCompleteMonth (user_input,index):     #fetches monthly data with daily merged graph
    try:
        user_provided_year_month = user_input[index].split('/')
        if len(user_provided_year_month) == 1 or len(user_provided_year_month) == 0:
            print('Invalid Input')
            keypress = input('Press any key to continue...')
            _main_()
        else:
             month = numberToWordsMapperForMonths (int(user_provided_year_month[1]))
             if month != -1:
                 filename = 'weatherfiles/Murree_weather_'+user_provided_year_month[0]+'_'+month+'.txt'
                 monthly_data = MonthlyWeather(filename)

                 if monthly_data.verifyDataForMonth():
                     monthly_data.readDataForDailyGraph()
                     sys.exit();
                 else:
                     print ('No record found against this month')
                     keypress = input('Press any key to continue...')
                     _main_()
    except IndexError:
        print('Invalid Input')
        keypress = input('Press any key to continue...')
        _main_()

def _main_ ():
    clearScreen()
    option = input('Enter option: ')
    yearly_data = '-e'
    monthly_data = '-a'
    monthly_data_with_graph = '-c'
    monthly_data_with_merged_graph = '-g'

    user_input = option.split(" ")
    for index,val in enumerate(user_input):
        if yearly_data in val:
            getDataForParticularYear (user_input,index+1)
        if monthly_data in val:
            getDataForParticularMonth (user_input,index+1)
        if monthly_data_with_graph in val:
            getDataInGraphForCompleteMonth (user_input,index+1)
        if monthly_data_with_merged_graph in val:
            getDailyGraphReportForCompleteMonth (user_input,index+1)

        keypress = input('Press any key to continue...')
        _main_()                                                 #main function

_main_()
