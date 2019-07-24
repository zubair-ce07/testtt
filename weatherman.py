import csv
import sys
import os
import operator
import calendar
from colorama import init
from colorama import Fore, Style


class WeatherMan:
    def __init__(self, path):
        self.__path = path+'//'

    def year_files(self, year):  # fettching year files
        year_files = []
        directory_files = os.listdir(self.__path)
        for file in directory_files:
            if str(year) in file:
                year_files.append(file)
        return year_files

    def highest_record_in_a_year(self, year):
        max_temperatures = []
        low_temperatures = []
        dates = []
        max_humidities = []

        files = self.year_files(year)  # given year files
        if len(files) == 0:
            print('No Data Found For This Year')
            return
        for file in files:  # looping over list of files
            with open(self.__path+file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)  # for skipping titles
                for row in csv_reader:
                    # checking if a field data is empth
                    if self.check_emptinesss(row[1]):
                        max_temperatures.append(int(row[1]))
                    if self.check_emptinesss(row[3]):
                        low_temperatures.append(int(row[3]))
                    if self.check_emptinesss(row[7]):
                        max_humidities.append(int(row[7]))
                    dates.append(row[0])

        # calculating maximum,minimum and max humidity
        max_temperature = max(max_temperatures)
        low_temperature = min(low_temperatures)
        max_humid = max(max_humidities)

        # prinitng values to console
        print('Highest: '+str(max_temperature)+'C on ' +
              self.get_and_format_date(dates, max_temperatures,
                                       max_temperature))
        print('Lowest: '+str(low_temperature)+'C on ' +
              self.get_and_format_date(dates, low_temperatures,
                                       low_temperature))
        print('Humid: '+str(max_humid)+'% on ' +
              self.get_and_format_date(dates, max_humidities, max_humid))

    # checking if the data inn argument is empty or not
    def check_emptinesss(self, data):
        if data == '':
            return False
        return True

    # getting date for a given filed and then formating that date to words
    def get_and_format_date(self, date_list, data_list, data):
        date = date_list[data_list.index(data)]
        date = date.split('-')
        month = date[1]
        day = date[2]
        month = calendar.month_abbr[int(month)]
        return month + ' ' + day

    # formating date to words
    def format_date(self, month, year):
        month = calendar.month_abbr[int(month)]
        return month + ' ' + year

    def average_record_in_a_month(self, date):
        # splitting date and year form the given date
        date = date.split('/')
        year = date[0]
        month = date[1]
        month = months[int(month)-1]  # months in words from months array
        highest_temp_average = 0
        lowest_temp_average = 0
        average_humidity = 0
        highest_temp_count = 0
        lowest_temp_count = 0
        humidity_count = 0

        try:
            with open(self.__path+'Murree_weather_'+year+'_' +
                      month+'.txt') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)  # skipping titiles
                for row in csv_reader:
                    # checkin if the filed is empty and then adding it to the
                    # averages for later use
                    if self.check_emptinesss(row[1]):
                        highest_temp_average += int(row[1])
                        highest_temp_count += 1
                    if self.check_emptinesss(row[3]):
                        lowest_temp_average += int(row[3])
                        lowest_temp_count += 1
                    if self.check_emptinesss(row[8]):
                        average_humidity += int(row[8])
                        humidity_count += 1

            # calculating average
            highest_temp_average = highest_temp_average // highest_temp_count
            lowest_temp_average = lowest_temp_average // lowest_temp_count
            average_humidity = average_humidity // humidity_count
            print('Highest Average: '+str(highest_temp_average)+'C')
            print('Lowest Average: '+str(lowest_temp_average)+'C')
            print('Average Humidity: '+str(average_humidity)+'%')
        except FileNotFoundError:
            print("Data does not exsist for this date")

    def split_date_into_date_year(date):
        date = date.split('/')
        year = date[0]
        month = date[1]

    def highest_lowest_temprature_of_a_day(self, date):
        # splitting date and year form the given date
        date = date.split('/')
        year = date[0]
        month = date[1]
        print(self.format_date(month, year))
        month = months[int(month)-1]  # months in words from months array

        try:
            with open(self.__path+'Murree_weather_'+year+'_' +
                      month+'.txt') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)  # skipping titiles
                day = 1
                for row in csv_reader:
                    if self.check_emptinesss(row[1]):
                            # printing bar charts
                        print(day, end=' ')
                        for _ in range(int(row[1])):
                            print(Fore.RED + '+', end='')
                        print(Fore.WHITE+str(' '+row[1]+'C'))
                        print(day, end=' ')
                        for _ in range(int(row[3])):
                            print(Fore.BLUE + '+', end='')
                        print(Fore.WHITE+str(' '+row[1]+'C'))
                        day += 1
        except FileNotFoundError:
            print('Data does not exsist for this date')

    def highest_lowest_temprature_of_a_day2(self, date):
        # splitting date and year form the given date
        date = date.split('/')
        year = date[0]
        month = date[1]
        print(self.format_date(month, year))
        month = months[int(month)-1]  # months in words from months array

        try:
            with open(self.__path+'Murree_weather_'+year+'_' +
                      month+'.txt') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)  # skipping titiles
                day = 1
                for row in csv_reader:
                    if self.check_emptinesss(row[1]):
                        print(day, end=' ')
                        for _ in range(int(row[3])):
                            print(Fore.BLUE + '+', end='')
                        for _ in range(int(row[1])):
                            print(Fore.RED + '+', end='')
                        print(Fore.WHITE+str(' '+row[1]+'C- '), end='')
                        print(''+Fore.WHITE+str(row[1]+'C'))
                        day += 1
        except FileNotFoundError:
            print("Data does not exsist for this date")


try:
    report_type = sys.argv[1]
    date = sys.argv[2]
    path = sys.argv[3]
except:
    print('File not executed properly')

months = [
    'Jan', 'Feb', 'Mar', 'Apr',
    'May', 'Jun', 'Jul', 'Aug',
    'Sep', 'Oct', 'Nov', 'Dec']

# w = WeatherMan('weatherfiles//')
w = WeatherMan(path)

if(report_type == '-e'):
    try:
        int(date)
        w.highest_record_in_a_year(date)
    except ValueError:
        print('Enter an intiger for year')
try:
    date.split('/')
    if(report_type == '-a'):
        w.average_record_in_a_month(date)
    if(report_type == '-c'):
        w.highest_lowest_temprature_of_a_day(date)
    if(report_type == '-d'):
        w.highest_lowest_temprature_of_a_day2(date)
except:
    print('Enter a valid intiger value and seperator for year and month')
