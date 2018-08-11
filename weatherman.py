"""
This module reads weather files and calculate max, min temprature and build charts
"""

from __future__ import print_function
import calendar
import os
import re
from termcolor import colored

class WeatherMan:
    """
    This class reads weather files and calculate max, min temprature, build charts
    and print in front of user
    """

    def __init__(self):
        self.path = ''
        self.file_name = []
        self.month_files = []
        self.max_temp_monthwise = []
        self.low_temp_monthwise = []
        self.date_monthwise = []
        self.humid = []

    # getting path of data files
    def get_path(self):
        """
         This function gets path of related files from a path.txt file
        """
        try:
            _file = open(os.getcwd()+'/path', "r")
            path_string = _file.read()
            path = path_string.strip()
            self.path = path

        except IOError:
            print('\nPlease place your path file in the same directory'
                  ' with the code file in phycharm default location')


    # clearing Global Variables after use
    def clear_variables(self):
        """
        This function clears all variables used at the end of program's iteration
        """
        self.file_name.clear()
        self.month_files.clear()
        self.max_temp_monthwise.clear()
        self.low_temp_monthwise.clear()
        self.date_monthwise.clear()
        self.humid.clear()


    # getting a specific year files
    def get_files(self, year):
        """
        This function gets file names of desired year
        """
        try:
            for files in os.listdir(self.path):
                if re.match('.*' + year + '.*', files):
                    self.file_name.append(files)
        except IOError:
            print('Files not found for this year')


    # getting a specific month file
    def get_single_file(self, year, month):
        """
        This function gets file name of desired month
        """
        try:
            for files in os.listdir(self.path):
                if re.match('.*' + year + '.*', files):
                    self.file_name.append(files)

            for _month in self.file_name:
                if re.match('.*' + month + '.*', _month):
                    self.month_files.append(_month)
        except IOError:
            print('File not found for this month')


    # reading data from year files
    def read_from_files(self):
        """
        This function reads files of desired year
        """
        for my_file in self.file_name:
            _file = (open(self.path + my_file, 'r'))
            for line in _file:
                collection = line.split(',')
                if collection[1] == '' or collection[3] == '' or collection[7] == '':
                    continue
                self.max_temp_monthwise.append(collection[1])
                self.low_temp_monthwise.append(collection[3])
                self.humid.append(collection[7])
                self.date_monthwise.append(collection[0])


    # reading data from file for a month
    def read_month_file(self):
        """
        This function reads file of desired month
        """
        for my_file in self.month_files:
            file1 = (open(self.path + my_file, 'r'))
            for line in file1:
                collection = line.split(',')
                if collection[1] == '' or collection[3] == '' or collection[7] == '':
                    continue
                self.max_temp_monthwise.append(collection[1])
                self.low_temp_monthwise.append(collection[3])
                self.humid.append(collection[7])
                self.date_monthwise.append(collection[0])


    # removing unnecessary elements(headers) from year files' container
    def removing_elements(self):
        """
        This function removes headers from max temp container for a year's data
        """
        count = 0
        while count < len(self.file_name):
            self.max_temp_monthwise.remove('Max TemperatureC')
            self.low_temp_monthwise.remove('Min TemperatureC')
            self.humid.remove('Max Humidity')
            if 'PKT' in self.date_monthwise:
                self.date_monthwise.remove('PKT')
            else:
                self.date_monthwise.remove('PKST')
            count += 1


    # removing unnecessary element(headers) from month file container
    def removing_element(self):
        """
        This function removes headers from max temp container just for a month data
        """
        count = len(self.month_files)
        if count > 0:
            self.max_temp_monthwise.remove('Max TemperatureC')
            self.low_temp_monthwise.remove('Min TemperatureC')
            self.humid.remove('Max Humidity')
            if 'PKT' in self.date_monthwise:
                self.date_monthwise.remove('PKT')
            else:
                self.date_monthwise.remove('PKST')
            self.temp_list_conversion()
        else:
            print('File not found for this month')


    # Converting max_temp_monthwise into integer list
    def temp_list_conversion(self):
        """
        This function converts string lists into integer lists for mathematical operations
        """
        self.max_temp_monthwise = list(map(int, self.max_temp_monthwise))
        self.low_temp_monthwise = list(map(int, self.low_temp_monthwise))
        self.humid = list(map(int, self.humid))


    # for average maximum, minimum temperature and maximum average humidity
    def show_average(self):
        """
        This function prints max and min average temperature and humidity
        """
        sum_max_temp = sum(self.max_temp_monthwise)
        sum_low_temp = sum(self.low_temp_monthwise)
        sum_humid = sum(self.humid)
        average_max_temp = int(sum_max_temp / len(self.max_temp_monthwise))
        average_low_temp = int(sum_low_temp / len(self.low_temp_monthwise))
        average_humid = int(sum_humid / len(self.humid))
        print('************************************')
        print('Highest Average: {average_max_temp}C '.format(
            average_max_temp=str(average_max_temp)))
        print('Lowest Average: {average_low_temp}C '.format(
            average_low_temp=str(average_low_temp)))
        print('Average Humidity: {average_humid}% '.format(
            average_humid=str(average_humid)))
        print('************************************')


    # Date Conversion
    def date_conversion(self, index):
        """
        This function converts numaric date into english date
        """
        raw_date = index
        raw_date = raw_date.split('-')
        complete_date = calendar.month_name[int(raw_date[1])]
        complete_date = complete_date + " " + raw_date[2]
        return complete_date


    # Print required information
    def print_data(self):
        """
        This function prints required output of user
        """
        max_value = max(self.max_temp_monthwise)
        min_value = min(self.low_temp_monthwise)
        max_humid = max(self.humid)
        index = self.max_temp_monthwise.index(max_value)
        min_index = self.low_temp_monthwise.index(min_value)
        humid_index = self.humid.index(max_humid)
        print('************************************')
        print('Highest: {max_temp}C on {date}'.format(max_temp=str(
            self.max_temp_monthwise[index]), date=self.date_conversion(self.date_monthwise[index])))
        print('Lowest: {low_temp}C on {date}'.format(low_temp=str(
            self.low_temp_monthwise[min_index]), date=self.date_conversion(
                self.date_monthwise[min_index])))
        print('Humidity: {humid}% on {date}'.format(humid=str(
            self.humid[humid_index]), date=self.date_conversion(
                self.date_monthwise[humid_index])))
        print('************************************')


    # Print chart
    def print_chart(self):
        """
        This function prints bar charts
        """
        for max_temp, min_temp, date in zip(self.max_temp_monthwise,
                                            self.low_temp_monthwise, self.date_monthwise):
            print('{date} {color} {m_temp}C'.format(
                date=date, color=colored('+'*max_temp, 'red'), m_temp=str(max_temp)))
            print('{date} {color} {m_temp}C'.format(
                date=date, color=colored('+'*min_temp, 'blue'), m_temp=str(min_temp)))


    # Bonus Task: Print both charts (bar charts) together
    def print_bar_chart(self):
        """
        This function prints horizontal bar charts
        """
        for max_temp, min_temp, date in zip(self.max_temp_monthwise,
                                            self.low_temp_monthwise,
                                            self.date_monthwise):
            print('{date} {color_blue} {color_red}{min_value}C {max_value}C'.format(
                date=date, color_blue=colored('+'*min_temp, 'blue'), color_red=colored(
                    '+'*max_temp, 'red'), min_value=str(min_temp), max_value=str(max_temp)))

# Main Method
def main():
    """
    This function is entry point of program
    """
    weather_man = WeatherMan()
    weather_man.get_path()
    while True:
        try:
            choice = int(input('Press 1 for year base information\nPress 2 for Month '
                               'base information\n'
                               'Press 3 to print chart\nPress 4 to make horizontal'
                               ' bar chart for each day\n'
                               'Press 5 exit: '))
            if choice == 1:
                year = str(input('Enter the year you want to get information: '))
                weather_man.get_files(year)
                weather_man.read_from_files()
                weather_man.removing_elements()
                weather_man.temp_list_conversion()
                weather_man.print_data()

            elif choice == 2:
                year = str(input('Enter the year you want to get information: '))
                month = str(input('Enter the month (i.e Jan): '))
                weather_man.get_single_file(year, month)
                weather_man.read_month_file()
                weather_man.removing_element()
                weather_man.show_average()

            elif choice == 3:
                year = str(input('Enter the year you want to get information: '))
                month = str(input('Enter the month (i.e Jan): '))
                weather_man.get_single_file(year, month)
                weather_man.read_month_file()
                weather_man.removing_element()
                weather_man.print_chart()

            elif choice == 4:
                year = str(input('Enter the year you want to get information: '))
                month = str(input('Enter the month (i.e Jan): '))
                weather_man.get_single_file(year, month)
                weather_man.read_month_file()
                weather_man.removing_element()
                weather_man.print_bar_chart()

            elif choice == 5:
                break

            else:
                print('Wrong choice')

                weather_man.clear_variables()
            choice = 0
            print("\n")

        except ValueError:
            print("Wrong value entered")
            weather_man.clear_variables()
            choice = 0


# execution point of program
if __name__ == '__main__':
    main()
