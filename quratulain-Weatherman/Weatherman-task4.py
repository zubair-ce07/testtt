from termcolor import colored
import argparse
import fnmatch
import math
import csv
import os


class Weatherman:
    # Function to generate report1
    def generate_report_one(self, files_records_dict, year):

        found = False
        max_temprature = float('-inf')
        max_temp_day = ''
        max_temp_month = ''

        min_temprature = float('inf')
        min_temp_day = ''
        min_temp_month = ''

        max_humidity = float('-inf')
        max_humid_day = ''
        max_humid_month = ''

        for file in files_records_dict.keys():
            file_name = 'Murree_weather_' + year + '_*.txt'

            if fnmatch.fnmatch(file, file_name):
                found = True
                max_temp_list = [(record['maxTemprature'], record['day'], record['month']) for record in
                                 files_records_dict[file]]
                min_temp_list = [(record['minTemprature'], record['day'], record['month']) for record in
                                 files_records_dict[file]]
                max_humid_list = [(record['maxHumidity'], record['day'], record['month']) for record in
                                  files_records_dict[file]]

                max_temp_tuple = max(max_temp_list)
                min_temp_tuple = min(min_temp_list)
                max_humid_tuple = max(max_humid_list)

                # Find the highest temprature, date and month of the given year
                if max_temp_tuple[0] > max_temprature:
                    max_temprature = max_temp_tuple[0]
                    max_temp_day = max_temp_tuple[1]
                    max_temp_month = max_temp_tuple[-1]

                # Find the lowest temprature, date and month of the given year
                if min_temp_tuple[0] < min_temprature:
                    min_temprature = min_temp_tuple[0]
                    min_temp_day = min_temp_tuple[1]
                    min_temp_month = min_temp_tuple[-1]

                # Find the highest humidity, date and month of the given year
                if max_humid_tuple[0] > max_humidity:
                    max_humidity = max_humid_tuple[0]
                    max_humid_day = max_humid_tuple[1]
                    max_humid_month = max_humid_tuple[-1]

        if found is True:
            print("Highest: {}C on {} {}".format(max_temprature, max_temp_month, max_temp_day))
            print("Lowest: {}C on {} {}".format(min_temprature, min_temp_month, min_temp_day))
            print("Humidity: {}% on {} {} \n".format(max_humidity, max_humid_month, max_humid_day))
        else:
            print("For report1: Record for this year doesn't exists \n")

    # Function to generate report2
    def generate_report_two(self, files_records_dict, year, month_name):

        file_name = 'Murree_weather_' + year + '_' + month_name + '.txt'
        file_record = files_records_dict.get(file_name)

        if file_record is not None:
            max_temp_list = [(record['maxTemprature']) for record in
                             file_record]
            min_temp_list = [(record['minTemprature']) for record in
                             file_record]
            mean_humid_list = [(record['meanHumidity']) for record in
                               file_record]

            max_temp_average = math.ceil(sum(max_temp_list) / len(max_temp_list))
            min_temp_average = math.ceil(sum(min_temp_list) / len(min_temp_list))
            mean_humid_average = math.ceil(sum(mean_humid_list) / len(mean_humid_list))

            print("Highest Average: {}C ".format(max_temp_average))
            print("Lowest Average: {}C ".format(min_temp_average))
            print("Mean Humidity Average: {}% \n".format(mean_humid_average))
        else:
            print("For Report2: Record for the given year/month doesn't exists \n")

    # Function to generate report3
    def generate_report_three(self, files_records_dict, year, month_name):

        file_name = 'Murree_weather_' + year + '_' + month_name + '.txt'
        file_record = files_records_dict.get(file_name)
        max_temp_output = ''
        min_temp_output = ''

        if file_record is not None:
            max_temp_list = [(record['maxTemprature']) for record in
                             file_record]
            min_temp_list = [(record['minTemprature']) for record in
                             file_record]
            days = [(record['day']) for record in
                    file_record]

            for day in days:
                # Print the highest temprature of each day of the given month
                max_temp = max_temp_list[day - 1]
                min_temp = min_temp_list[day - 1]

                if max_temp is not float('-inf'):
                    max_temp_output = colored(day, 'red')
                    for i in range(1, max_temp):
                        max_temp_output = max_temp_output + colored('+', 'red')
                    max_temp_output = max_temp_output + colored(str(max_temp) + 'C', 'red')

                if min_temp is not float('inf'):
                    min_temp_output = colored(day, 'blue')
                    for i in range(1, min_temp):
                        min_temp_output = min_temp_output + colored('+', 'blue')
                    min_temp_output = min_temp_output + colored(str(min_temp) + 'C', 'blue')
                else:
                    continue

                print(max_temp_output)
                print(min_temp_output)

        # Output the result if record is found.
        else:
            print("For report3: Record for this month doesn't exists")


'''
Class Ends
'''

'''
Functions to Validate Arguments
'''


def validate_arguments_year(argreport1):
    if len(argreport1) != 4:
        raise argparse.ArgumentTypeError('Please enter the valid year e.g. 2009')
    else:
        return argreport1


def validate_arguments_month_year(argreport):
    date = argreport.split('/')

    if len(date) != 2:
        raise argparse.ArgumentTypeError('Please enter the valid year/month e.g. 2009/2')
    if date[-1] == '':
        raise argparse.ArgumentTypeError('Please enter the month e.g. 2009/2')
    if date[-1] < 13 and date[-1] > 0:
        raise argparse.ArgumentTypeError('Please enter the valid month e.g. 2009/2')

    return argreport


def get_month_name(month):
    monthList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return monthList[month - 1] if month < 13 and month > 0 else ''


# Read the given files and maintain a dictionary
# having file records in the form of list of dictionaries.
def read_files(dirPath, arg_value_list):
    file_data = []
    files_data = {}

    for arg in arg_value_list:
        year = arg[0]
        month_name = arg[-1]
        file_name = 'Murree_weather_' + year + '_' + month_name + '.txt'

        for file in os.listdir(dirPath):
            if fnmatch.fnmatch(file, file_name) and file_name not in files_data:
                with open(args.dirPath + '/' + file, "r") as current_file:
                    reader = csv.DictReader(current_file)

                    for row in reader:
                        record_date = row['PKT'] if row.get('PKST') is None else row['PKST']
                        max_temprature = float('-inf') if row['Max TemperatureC'] is '' else int(
                            row['Max TemperatureC'])
                        min_temprature = float('inf') if row['Min TemperatureC'] is '' else int(row['Min TemperatureC'])
                        max_humidity = float('-inf') if row['Max Humidity'] is '' else int(row['Max Humidity'])
                        mean_humidity = float('inf') if row[' Mean Humidity'] is '' else int(row[' Mean Humidity'])
                        year, month, day = record_date.split('-')
                        month_name = get_month_name(int(month))

                        file_data.append({

                            'day': int(day),
                            'year': int(year),
                            'month': month_name,
                            'maxHumidity': max_humidity,
                            'meanHumidity': mean_humidity,
                            'minTemprature': min_temprature,
                            'maxTemprature': max_temprature,

                        })

                    files_data[file] = file_data
                    file_data = []

    return files_data


'''
Main Method
'''

if __name__ == "__main__":

    year = ''
    month = ''
    arg_dict = {}
    is_rep1_generated = False
    is_rep2_generated = False
    is_rep3_generated = False

    # Parse the given arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("dirPath", help="the path of directory where files are allocated")
    parser.add_argument("-e", "--argreport1", type=validate_arguments_year,
                        help="specify year for required information")
    parser.add_argument("-c", "--argreport2", type=validate_arguments_month_year,
                        help="specify month for required information")
    parser.add_argument("-a", "--argreport3", type=validate_arguments_month_year,
                        help="specify month for required information")

    args = parser.parse_args()

    # Form a list of arguments.
    if args.argreport1 is not None:
        year = args.argreport1
        month = '*'
        arg_dict['e'] = [year, month]

    if args.argreport2 is not None:
        year, month = args.argreport2.split('/')
        month_name = get_month_name(int(month))
        arg_dict['c'] = [year, month_name]

    if args.argreport3 is not None:
        year, month = args.argreport3.split('/')
        month_name = get_month_name(int(month))
        arg_dict['a'] = [year, month_name]

    # Save the data of the required files, in the form of dictionary of files.
    if arg_dict:
        files_dict = read_files(args.dirPath, arg_dict.values())
        weatherman = Weatherman()

        # Generate reports.
        for report in arg_dict.keys():
            if 'e' in arg_dict and is_rep1_generated == False:
                print('Report1: ')
                weatherman.generate_report_one(files_dict, year)
                is_rep1_generated = True

            elif 'c' in arg_dict and is_rep2_generated == False:
                print('Report2: ')
                weatherman.generate_report_two(files_dict, year, month_name)
                is_rep2_generated = True

            elif 'a' in arg_dict and is_rep3_generated == False:
                print('Report3: \n ' + month_name + ' ' + year)
                weatherman.generate_report_three(files_dict, year, month_name)
                is_rep3_generated = True
