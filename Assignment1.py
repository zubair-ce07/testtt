import glob
import os
import csv
import argparse


# calculate the min and max values
def weather_compare(date, max_temp, min_temp,
                    max_humidity, min_humidity, year, weather_info):
    if max_temp:
        if int(max_temp) > int(weather_info[year]['Max_Temp_Dic']['Max_Temp']):
            weather_info[year]['Max_Temp_Dic']['Max_Temp'] = max_temp
            weather_info[year]['Max_Temp_Dic']['date'] = date

    if min_temp:
        if int(min_temp) < int(weather_info[year]['Min_Temp_Dic']['Min_Temp']) or not \
                weather_info[year]['Min_Temp_Dic']['Min_Temp']:
            weather_info[year]['Min_Temp_Dic']['Min_Temp'] = min_temp
            weather_info[year]['Min_Temp_Dic']['date'] = date

    if max_humidity:
        if int(max_humidity) > int(weather_info[year]['Max_Humidity']):
            weather_info[year]['Max_Humidity'] = max_humidity

    if min_humidity:
        if int(min_humidity) < int(weather_info[year]['Min_Humidity']) or not \
                weather_info[year]['Min_Humidity']:
            weather_info[year]['Min_Humidity'] = min_humidity


# assign values to empty parameters
def replace_empty_values(year, weather_info):
    if not weather_info[year]['Max_Temp_Dic']['Max_Temp']:
        weather_info[year]['Max_Temp_Dic']['Max_Temp'] = -1000

    if not weather_info[year]['Min_Temp_Dic']['Min_Temp']:
        weather_info[year]['Min_Temp_Dic']['Min_Temp'] = 1000

    if not weather_info[year]['Max_Humidity']:
        weather_info[year]['Max_Humidity'] = -1000

    if not weather_info[year]['Min_Humidity']:
        weather_info[year]['Min_Humidity'] = 1000


# Read data From File
def read_weather_data(data_directory, weather_info):
    os.chdir(data_directory)
    for file_name in glob.glob("*.txt"):
        with open(file_name) as csvfile:
            next(csvfile, None)
            file_data = csv.DictReader(csvfile)
            for weather_variables in file_data:
                if 'PKT' in weather_variables:
                    collect_results(weather_variables['PKT'], weather_variables, weather_info)
                else:
                    collect_results(weather_variables['PKST'], weather_variables, weather_info)


def collect_results(date, weather_variables, weather_info):
    year = date.split('-')
    if year[0] not in weather_info and len(year[0]) > 2:
        weather_info[year[0]] = {'Max_Temp_Dic': {'date': date,
                                                  'Max_Temp': weather_variables['Max TemperatureC']},
                                 'Min_Temp_Dic': {'date': date,
                                                  'Min_Temp': weather_variables['Min TemperatureC']},
                                 'Max_Humidity': weather_variables['Max Humidity'],
                                 'Min_Humidity': weather_variables[' Min Humidity']}
        replace_empty_values(year[0], weather_info)
    elif len(year[0]) > 2:
        weather_compare(date, weather_variables['Max TemperatureC'],
                        weather_variables['Min TemperatureC'], weather_variables['Max Humidity'],
                        weather_variables[' Min Humidity'], year[0], weather_info)


def report_annual(weather_info):
    print "Annual Max/Min Temperature" + '\n'
    print "   Year  " + "MAX Temp   " + "MIN Temp   " + "MAX Humidity   " + "MIN Humidity   "
    print '\n' + "   -------------------------------------------------------------------------"
    for key in weather_info:
        print "   " + key + "        " + weather_info[key]['Max_Temp_Dic']['Max_Temp'] + "         " + \
              weather_info[key]['Min_Temp_Dic']['Min_Temp'] + "         " + weather_info[key][
                  'Max_Humidity'] + "             " + weather_info[key]['Min_Humidity']
    print '\n'


def report_coldestday(weather_info):
    print "Coldest  Day Of Each Year" + '\n'
    print "   Year   " + "  Date    " + "MAX Temp"
    print '\n' + "   ------------------------------------"
    for key in weather_info:
        print "   " + key + "   " + weather_info[key]['Max_Temp_Dic']['date'] + "     " + \
              weather_info[key]['Max_Temp_Dic']['Max_Temp']
    print '\n'


def report_hottestday(weather_info):
    print "Hottest Day of Each Year" '\n'
    print "   Year   " + "  Date    " + "MIN Temp"
    print '\n' + "   ------------------------------------"
    for key in weather_info:
        print "   " + key + "   " + weather_info[key]['Min_Temp_Dic']['date'] + "     " + \
              weather_info[key]['Min_Temp_Dic']['Min_Temp']
    print '\n'


def get_args():
    parser = argparse.ArgumentParser()
    # Add arguments
    parser.add_argument(
            '-r', '--report', type=str)
    parser.add_argument(
            '-d', '--directory', type=str)
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    report = args.report
    directory = args.directory
    # Return all variable values
    return directory, report


def main():
    parameters = get_args()
    weather_info = {}
    if parameters[0] and parameters[1]:
        read_weather_data(parameters[0], weather_info)
        if parameters[1] == '1':
            report_annual(weather_info)

        if parameters[1] == '2':
            report_coldestday(weather_info)

        if parameters[1] == '3':
            report_hottestday(weather_info)
    else:
        print '\nUsage:   weatherman \n'
        print '[Report #] \n1 for Annual Max/Min Temperature \n' \
              '2 for Hottest day of each year \n3 for coldest day of each year \n'
        print '[data_dir] \nDirectory containing weather data files \n'
        print 'For Example : python Assignment1.py -r 1 -d /project/weatherdata'


if __name__ == "__main__":
    main()
