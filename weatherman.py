import argparse
import calendar
from termcolor import colored

filename = "/lahore_weather_[year]_[month].txt"
months = calendar.month_name

def display_highest_lowest(args):
    if (not args):
        return

    highest_temp = None
    lowest_temp = None
    highest_humidity = None
    highest_day = None
    highest_month = None
    lowest_day = None
    lowest_month = None
    humidity_day = None
    humidity_month = None

    for month in months[1:]:
        cur_filename = args[1] + filename.replace('[year]', args[0])
        cur_filename = cur_filename.replace('[month]', month[:3])
        try:
            file = open(cur_filename, "r")
        except IOError:
            #print('No file found!')
            continue

        lines = file.readlines()
        for line in lines[2:]:
            day_data = line.split(',')
            date = day_data[0].split('-')

            if(1<len(day_data) and day_data[1]
                                and (not highest_temp or highest_temp < int(day_data[1])) ):

                highest_temp = int(day_data[1])
                highest_day = date[2]
                highest_month = month

            if(3<len(day_data) and day_data[3]
                                and (not lowest_temp or lowest_temp > int(day_data[3])) ):

                lowest_temp = int(day_data[3])
                lowest_day = date[2]
                lowest_month = month

            if(7<len(day_data) and day_data[7]
                                and (not highest_humidity or highest_humidity < int(day_data[7])) ):

                highest_humidity = int(day_data[7])
                humidity_day = date[2]
                humidity_month = month

    print ('Highest: '+str(highest_temp)+ 'C'+' on '+highest_month+ ' '+highest_day
    + '\nLowest: '+str(lowest_temp)+'C' ' on '+lowest_month+' '+lowest_day
    + '\nHumid: '+str(highest_humidity)+'%'+' on '+humidity_month+' '+humidity_day)

def display_average(args):
    if (not args):
        return

    highest_temp = None
    lowest_temp = None
    highest_humidity = None

    date = args[0].split('/')

    cur_filename = args[1] + filename.replace('[year]', date[0])
    cur_filename = cur_filename.replace('[month]', months[int(date[1])][:3])
    try:
        file = open(cur_filename, "r")
    except IOError:
        print('No file found!')
        return

    lines = file.readlines()
    for line in lines[2:]:
        day_data = line.split(',')
        if (2 < len(day_data) and day_data[2]
                                and (not highest_temp or highest_temp < int(day_data[2])) ):
            highest_temp = int(day_data[2])

        if (2 < len(day_data) and day_data[2]
                                and (not lowest_temp or lowest_temp > int(day_data[2])) ):
            lowest_temp = int(day_data[2])

        if (8 < len(day_data) and day_data[8]
                                and (not highest_humidity or highest_humidity < int(day_data[8])) ):
            highest_humidity = int(day_data[8])

    print('Highest Average: ' + str(highest_temp) + 'C'
        + '\nLowest Average: ' + str(lowest_temp) + 'C'
        +'\nAverage Humidity: ' + str(highest_humidity) + '%')

def display_barCharts(args):
    if(not args):
        return

    date = args[0].split('/')
    print(months[int(date[1])] + ' ' + date[0])

    cur_filename = args[1] + filename.replace('[year]', date[0])
    cur_filename = cur_filename.replace('[month]', months[int(date[1])][:3])
    try:
        file = open(cur_filename, "r")
    except IOError:
        print('No file found!')
        return

    lines = file.readlines()
    for line in lines[2:]:
        day_data = line.split(',')
        cur_date = day_data[0].split('-')

        if (1 < len(day_data) and day_data[1]):
            highest_temp = int(day_data[1])

            print(cur_date[2] + ' ', end='')

            for index in range(highest_temp):
                print(colored('+', 'red'), end='')
            print(' ' + str(highest_temp) + 'C')

        if (3 < len(day_data) and day_data[3]):
            lowest_temp = int(day_data[3])

            print(cur_date[2] + ' ', end='')

            for index in range(lowest_temp):
                print(colored('+', 'blue'), end='')
            print(' ' + str(lowest_temp) + 'C')

    print('\n')

    for line in lines[2:]:
        day_data = line.split(',')

        highest_temp = None
        lowest_temp = None
        if (3 < len(day_data) and day_data[3]):
            lowest_temp = int(day_data[3])

            print(day_data[0].split('-')[2] + ' ', end='')

            for index in range(lowest_temp):
                print(colored('+', 'blue'), end='')

        if(1<len(day_data) and day_data[1]):
            highest_temp = int(day_data[1])

            for index in range(highest_temp):
                print(colored('+', 'red'), end='')

        if (lowest_temp and highest_temp):
            print(' ' + str(lowest_temp) + 'C' +'-'+ str(highest_temp) + 'C')


parser = argparse.ArgumentParser()
parser.add_argument('-e', nargs=2)
parser.add_argument('-a', nargs=2)
parser.add_argument('-c', nargs=2)
args = parser.parse_args()

display_highest_lowest(args.e)
display_average(args.a)
display_barCharts(args.c)