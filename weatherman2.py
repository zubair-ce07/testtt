import os
import re
import csv
import argparse

from enum import Enum


class REPORT_NUMBER(Enum):
    basicweatherreport = 1
    hottestdayreport = 2
    coolestdayreport = 3


def reading_and_processing_data_from_files(reader, stats, year, min_temps, min_hums):
    for row in reader:
        max_temp = row.get('Max TemperatureC')
        min_temp = row.get('Min TemperatureC')
        max_hum = row.get('Max Humidity')
        min_hum = row.get(' Min Humidity')
        row_date = row.get('PKT') or row.get('PKST')

        if max_temp:  # Calculating maximum temperature & respective date
            x = int(max_temp)
            if stats[year]['Max-tempC'] < x:
                stats[year]['Max-tempC'] = x
                stats[year]['Max-Temp-date'] = row_date

        if min_temp:  # Adding minimum temperatures & dates in  minimum_temperatures_dictionary
            min_temps[row_date] = min_temp

        if max_hum:  # Calculating maximum humidity
            x = int(max_hum)
            if stats[year]['Max-Hum'] < x:
                stats[year]['Max-Hum'] = x

        if min_hum:
            min_hums.append(min_hum)

    min_temp_date = ''
    min_temp_value = 0
    min_hum_value = 0

    '''Calculating minimum temperature of each year and
        respective date in following block of code'''
    if min_temps:
        min_temp_date = min(min_temps, key=min_temps.get)
        min_temp_value = min(min_temps.values())
    if not stats[year]['Min-TempC']:
        stats[year]['Min-TempC'] = int(min_temp_value)
        stats[year]['Min-Temp-date'] = min_temp_date
    else:
        if stats[year]['Min-TempC'] > int(min_temp_value):
            stats[year]['Min-TempC'] = int(min_temp_value)
            stats[year]['Min-Temp-date'] = min_temp_date

    '''Calculating minimum humidity'''
    if min_hums:
        min_hum_value = min(min_hums)
    if not stats[year]['Min-Hum']:
        stats[year]['Min-Hum'] = int(min_hum_value)
    else:
        if stats[year]['Min-Hum'] > int(min_hum_value):
            stats[year]['Min-Hum'] = int(min_hum_value)


'''
This function calculates all required parameters and
stores them in a dictionary & return in the end.
'''


def getting_weather_report(data_path):
    weatherman_report_data = {}
    for filename in os.listdir(data_path):
        file_path = os.path.join(data_path, filename)
        with open(file_path) as csvfile:
            name = csvfile.name
            year = (re.split('_', name))
            file_year = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            minimum_humidities = []  # To store 'Min Temperature' key values of a file.'''
            minimum_temperatures_and_dates = {}
            ''' Above dictionary has a key date & minimum temperature
                on that day as value & datea of key values of a file.'''

            if file_year in weatherman_report_data:  # Updating values of existing key
                reading_and_processing_data_from_files(reader,
                                                       weatherman_report_data, file_year,
                                                       minimum_temperatures_and_dates,
                                                       minimum_humidities)

            else:  # Adding a new key
                weatherman_report_data[file_year] = {'Max-tempC': 0, 'Min-TempC': 0, 'Max-Hum': 0,
                                                     'Min-Hum': 0, 'Max-Temp-date': '', 'Min-Temp-date': ''}
                reading_and_processing_data_from_files(reader,
                                                       weatherman_report_data, file_year,
                                                       minimum_temperatures_and_dates,
                                                       minimum_humidities)
    return weatherman_report_data


'''
This function basic_weather_report outputs formatted
report containg maximum temperature, minimum temperature,
maximum humidity & minimum humidity yearly.
'''


def basic_weather_Report(absolute_data_path):
    weather_report = getting_weather_report(absolute_data_path)
    print("Year" + "  " + "Maximum Temprature " + "  " + "Minimum Temprature" +
          "   " + "Maximum Humidity" + "   " + "Minimum Humidity")
    print("-----------------------------------------------------------------------------------")
    for key in weather_report:
        print('{0: <16} {1: <16} {2: <16} {3: <16} {4: <16}'.format(key, weather_report.get(key)['Max-tempC'],
              weather_report.get(key)['Min-TempC'],
              weather_report.get(key)['Max-Hum'],  weather_report.get(key)['Min-Hum']))


'''
This function outputs formatted report comtaing
maximum temperature & date of that day.
'''


def hottest_day_of_each_year(absolute_data_path):
    weather_report = getting_weather_report(absolute_data_path)
    print("This is report# 2")
    print("year" '\t\t'"Date"'\t\t'"Temp")
    print("--------------------------------------------")
    for key in weather_report:
        print('{0: <16} {1: <16} {2: <16}'.format(key, weather_report.get(key)['Max-Temp-date'],
              weather_report.get(key)['Max-tempC']))


'''
This function outputs formatted report comtaing
minimum temperature & date of that day.
'''


def coolest_day_of_each_year(absolute_data_path):
    weather_report = getting_weather_report(absolute_data_path)
    print("This is report# 3")
    print("year"'\t\t'+ "Date"'\t\t' "Temp")
    print("--------------------------------------------")
    for key in weather_report:
        print('{0: <16} {1: <16} {2: <16}'.format(key, weather_report.get(key)['Min-Temp-date'],
                                                  weather_report.get(key)['Min-TempC']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reportnumber", help="input the report number", type=int)
    parser.add_argument("weatherdatapath", help="input the path that contains data files")
    args = parser.parse_args()
    report_no = args.reportnumber
    weatherdata_path = args.weatherdatapath
    if os.path.exists(weatherdata_path):
        if report_no == REPORT_NUMBER.basicweatherreport.value:
            basic_weather_Report(weatherdata_path)
        elif report_no == REPORT_NUMBER.hottestdayreport.value:
            hottest_day_of_each_year(weatherdata_path)
        elif report_no == REPORT_NUMBER.coolestdayreport.value:
            coolest_day_of_each_year(weatherdata_path)
        else:
            print("No such report found /n"
                  "select correct report number")


if __name__ == '__main__':
    main()

