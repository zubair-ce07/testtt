import os
import re
import csv
import argparse

from enum import Enum


class Report_number(Enum):
    basicweatherreport = 1
    hottestdayreport = 2
    coolestdayreport = 3


'''
For report 1 each key value has a dictianry with four keys as its value.
Those four keys are 'Max-TempC', 'Min-TempC','Max-Hum' & 'Min-Hum.
'''


def basic_weather_report_of_every_year():
    weatherman_report_data = {}
    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            name = csvfile.name
            year = (re.split('_', name))
            file_year = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            minimum_temperatures = []       # To store 'Min TemperatureC' key values of a file.
            minimum_humidities = []         # To store 'Min Temperature' key values of a file.

            if file_year in weatherman_report_data:  # Updating values of existing key
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    minimum_temperature = row.get('Min TemperatureC')
                    maximum_humidity = row.get('Max Humidity')
                    minimum_humidity = row.get(' Min Humidity')

                    if maximum_temperature:  # Calculating maximum temperature
                        x = int(maximum_temperature)
                        if weatherman_report_data[file_year]['Max-tempC'] < x:
                            weatherman_report_data[file_year]['Max-tempC'] = x

                    if minimum_temperature:
                        minimum_temperatures.append(minimum_temperature)

                    if maximum_humidity:  # Calculating maximum humidity
                        x = int(maximum_humidity)
                        if weatherman_report_data[file_year]['Max-Hum'] < x:
                            weatherman_report_data[file_year]['Max-Hum'] = x

                    if minimum_humidity:
                        minimum_humidities.append(minimum_humidity)
            else:
                weatherman_report_data[file_year] = {'Max-tempC': 0, 'Min-TempC': 0, 'Max-Hum': 0,
                                                     'Min-Hum': 0}  # Adding a new key
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    minimum_temperature = row.get('Min TemperatureC')
                    maximum_humidity = row.get('Max Humidity')
                    minimum_humidity = row.get(' Min Humidity')

                    if maximum_temperature:
                        x = int(maximum_temperature)
                        if weatherman_report_data[file_year]['Max-tempC'] < x:
                            weatherman_report_data[file_year]['Max-tempC'] = x

                    if minimum_temperature:
                        minimum_temperatures.append(minimum_temperature)

                    if maximum_humidity:
                        x = int(maximum_humidity)
                        if weatherman_report_data[file_year]['Max-Hum'] < x:
                            weatherman_report_data[file_year]['Max-Hum'] = x

                    if minimum_humidity:
                        minimum_humidities.append(minimum_humidity)

            if minimum_temperatures:
                min_temp_value = min(minimum_temperatures)
                x = int(min_temp_value)
            if not weatherman_report_data[file_year]['Min-TempC']:
                weatherman_report_data[file_year]['Min-TempC'] = x
            else:
                if weatherman_report_data[file_year]['Min-TempC'] > x:
                    weatherman_report_data[file_year]['Min-TempC'] = x

            if minimum_humidities:
                min_temp_value = min(minimum_humidities)
                x = int(min_temp_value)
            if not weatherman_report_data[file_year]['Min-Hum']:
                weatherman_report_data[file_year]['Min-Hum'] = x
            else:
                if weatherman_report_data[file_year]['Min-Hum'] > x:
                    weatherman_report_data[file_year]['Min-Hum'] = x

    print("This is report# 1")
    print(
        "Year" + "  " + "Maximum Temprature " + "  " + "Minimum Temprature" + "   " + "Maximum Humidity" + "   " + "Minimum Humidity")
    print("-----------------------------------------------------------------------------------")

    for key in weatherman_report_data:
        print(key, '\t\t', weatherman_report_data.get(key)['Max-tempC'], '\t\t',
              weatherman_report_data.get(key)['Min-TempC'], '\t\t',
              weatherman_report_data.get(key)['Max-Hum'], '\t\t', weatherman_report_data.get(key)['Min-Hum'])


'''
For this report each key in weather_report_data dictionary has a dictionary value which has further two key.
One is 'Date' to store hottest day of year & second is 'Max-TempC to store the temperature on that day'
'''

def find_hottest_day_of_every_year_report2():  # It will generate weather report about hottest day of each year.
    weatherman_report_data = {}
    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            name = csvfile.name
            year = (re.split('_', name))
            file_year = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            if file_year in weatherman_report_data:
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    if maximum_temperature:
                        x = int(maximum_temperature)
                        if weatherman_report_data[file_year]['Max-TempC'] < x:
                            weatherman_report_data[file_year]['Max-TempC'] = x

            else:
                weatherman_report_data[file_year] = {'Max-TempC': 0, 'Date': ''}
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    if maximum_temperature:
                        x = int(maximum_temperature)
                        if weatherman_report_data[file_year]['Max-TempC'] < x:
                            weatherman_report_data[file_year]['Max-TempC'] = x

    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            name = csvfile.name
            year = (re.split('_', name))
            file_year = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            HeaderList = reader.fieldnames
            if file_year in weatherman_report_data:
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    if maximum_temperature:
                        x = int(maximum_temperature)
                        if x == weatherman_report_data[file_year]['Max-TempC']:
                            weatherman_report_data[file_year]['Date'] = row.get('PKT') or row.get('PKST')

    print("This is report# 2")
    print("year" + "              " + "Date" + "                " + "Temp")
    print("--------------------------------------------")
    for keys in weatherman_report_data:
        print(keys, '\t\t', (weatherman_report_data[keys]['Date']), '\t\t',
              weatherman_report_data[keys]['Max-TempC'])

'''
For this report each key in weather_report_data dictionary has a dictionary value which has further two key.
One is 'Date' to store coolest day of year & second is 'Min-tempC to store the temperature on that day'
'''


def find_coolest_day_of_every_year_report3():  # It will report the coolest day of each year.
    weatherman_report_data = {}
    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            name = csvfile.name
            minimum_temperatures = []  # To store 'Min TemperatureC' key values of a file
            year = (re.split('_', name))
            file_year = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            if file_year in weatherman_report_data:
                for row in reader:
                    minimum_temperature = row.get('Min TemperatureC')
                    if minimum_temperature:
                        minimum_temperatures.append(minimum_temperature)
            else:
                weatherman_report_data[file_year] = {'Min-tempC': 0, 'Date': ''}
                for row in reader:
                    minimum_temperature = row.get('Min TemperatureC')
                    if minimum_temperature:
                        minimum_temperatures.append(minimum_temperature)

        if minimum_temperatures:
            min_temp_value = min(minimum_temperatures)
            x = int(min_temp_value)

        if not weatherman_report_data[file_year]['Min-tempC']:
            weatherman_report_data[file_year]['Min-tempC'] = x
        else:
            if weatherman_report_data[file_year]['Min-tempC'] > x:
                weatherman_report_data[file_year]['Min-tempC'] = x

    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            name = csvfile.name
            year = (re.split('_', name))
            file_year = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            HeaderList = reader.fieldnames
            if file_year in weatherman_report_data:
                for row in reader:
                    minimum_temperature = row.get('Min TemperatureC')
                    if minimum_temperature:
                        x = int(minimum_temperature)
                        if x == weatherman_report_data[file_year]['Min-tempC']:
                            weatherman_report_data[file_year]['Date'] = row.get('PKT') or row.get('PKST')

    print("This is report# 3")
    print("year" +"               " + "Date" + "               "+ "Temp")
    print("--------------------------------------------")
    for keys in weatherman_report_data:
        print(keys, '\t\t', (weatherman_report_data[keys]['Date']), '\t\t', weatherman_report_data[keys]['Min-tempC'])


if __name__ == '__main__':
    print(Report_number.basicweatherreport)
    parser = argparse.ArgumentParser()

    parser.add_argument("Reportnumber", help="input the report number", type=int)
    parser.add_argument("data_dir", help="input the path that contains data files")
    args = parser.parse_args()
    Report_no = args.Reportnumber
    dir = args.data_dir

    os.chdir("..")
    os.chdir(dir)
    dir = os.getcwd()

    if Report_no == Report_number.basicweatherreport.value:
        basic_weather_report_of_every_year()
    elif Report_no == Report_number.hottestdayreport.value:
        find_hottest_day_of_every_year_report2()
    elif Report_no == Report_number.coolestdayreport.value:
        find_coolest_day_of_every_year_report3()
    else:
        print("No such report found /n"
              "select correct report number")

