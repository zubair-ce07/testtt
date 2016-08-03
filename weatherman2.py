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
This function calculates all required parameters and
stores them in a dictionary & return in the end.
'''


def getting_weather_report_dictionary():
    weatherman_report_data = {}
    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            name = csvfile.name
            year = (re.split('_', name))
            file_year = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            minimum_humidities = []                 # To store 'Min Temperature' key values of a file.
            minimum_temperatures_dictionary = {}    # This dictionary has a key date & minimum temperature
                                                    # on that day as value & datea of key values of a file.

            if file_year in weatherman_report_data:  # Updating values of existing key
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    minimum_temperature = row.get('Min TemperatureC')
                    maximum_humidity = row.get('Max Humidity')
                    minimum_humidity = row.get(' Min Humidity')
                    date_ = row.get('PKT') or row.get('PKST')

                    if maximum_temperature:  # Calculating maximum temperature
                        x = int(maximum_temperature)
                        if weatherman_report_data[file_year]['Max-tempC'] < x:
                            weatherman_report_data[file_year]['Max-tempC'] = x
                            weatherman_report_data[file_year]['Max-Temp-date'] = date_

                    if minimum_temperature:   # Adding minimum temperatures & dates in  minimum_temperatures_dictionary
                        minimum_temperatures_dictionary[date_] = minimum_temperature

                    if maximum_humidity:     # Calculating maximum humidity
                        x = int(maximum_humidity)
                        if weatherman_report_data[file_year]['Max-Hum'] < x:
                            weatherman_report_data[file_year]['Max-Hum'] = x

                    if minimum_humidity:
                        minimum_humidities.append(minimum_humidity)
            else:
                # Adding a new key
                weatherman_report_data[file_year] = {'Max-tempC': 0, 'Min-TempC': 0, 'Max-Hum': 0,
                                                     'Min-Hum': 0, 'Max-Temp-date':'', 'Min-Temp-date':''}
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    minimum_temperature = row.get('Min TemperatureC')
                    maximum_humidity = row.get('Max Humidity')
                    minimum_humidity = row.get(' Min Humidity')
                    date_ = row.get('PKT') or row.get['PKST']

                    if maximum_temperature:
                        x = int(maximum_temperature)
                        if weatherman_report_data[file_year]['Max-tempC'] < x:
                            weatherman_report_data[file_year]['Max-tempC'] = x
                            weatherman_report_data[file_year]['Max-Temp-date']=date_

                    if minimum_temperature:
                        minimum_temperatures_dictionary[date_] = minimum_temperature

                    if maximum_humidity:
                        x = int(maximum_humidity)
                        if weatherman_report_data[file_year]['Max-Hum'] < x:
                            weatherman_report_data[file_year]['Max-Hum'] = x

                    if minimum_humidity:
                        minimum_humidities.append(minimum_humidity)

            if minimum_temperatures_dictionary:
                min_temp_date = min(minimum_temperatures_dictionary, key=minimum_temperatures_dictionary.get)
                min_temp_value = min(minimum_temperatures_dictionary.values())
                x = int(min_temp_value)
            if not weatherman_report_data[file_year]['Min-TempC']:
                weatherman_report_data[file_year]['Min-TempC'] = x
                weatherman_report_data[file_year]['Min-Temp-date'] = min_temp_date
            else:
                if weatherman_report_data[file_year]['Min-TempC'] > x:
                    weatherman_report_data[file_year]['Min-TempC'] = x
                    weatherman_report_data[file_year]['Min-Temp-date'] = min_temp_date

            if minimum_humidities:
                min_temp_value = min(minimum_humidities)
                x = int(min_temp_value)
            if not weatherman_report_data[file_year]['Min-Hum']:
                weatherman_report_data[file_year]['Min-Hum'] = x
            else:
                if weatherman_report_data[file_year]['Min-Hum'] > x:
                    weatherman_report_data[file_year]['Min-Hum'] = x

    return weatherman_report_data


'''
This function basic_weather_report outputs formatted
report containg maximum temperature, minimum temperature,
maximum humidity & minimum humidity yearly.
'''


def basic_weather_Report():
    weather_report = getting_weather_report_dictionary()
    print("Year" + "  " + "Maximum Temprature " + "  " + "Minimum Temprature" +
          "   " + "Maximum Humidity" + "   " + "Minimum Humidity")
    print("-----------------------------------------------------------------------------------")
    for key in weather_report:
        print(key, '\t\t', weather_report.get(key)['Max-tempC'], '\t\t',
              weather_report.get(key)['Min-TempC'], '\t\t',
              weather_report.get(key)['Max-Hum'], '\t\t', weather_report.get(key)['Min-Hum'])


'''
This function outputs formatted report comtaing
maximum temperature & date of that day.
'''


def hottest_day_of_each_year():
    weather_report = getting_weather_report_dictionary()
    print("This is report# 2")
    print("year" + "              " + "Date" + "                " + "Temp")
    print("--------------------------------------------")
    for key in weather_report:
        print(key, '\t\t', weather_report.get(key)['Max-Temp-date'], '\t\t',
              weather_report.get(key)['Max-tempC'])


'''
This function outputs formatted report comtaing
minimum temperature & date of that day.
'''
def coolest_day_of_each_year():
    weather_report = getting_weather_report_dictionary()
    print("This is report# 3")
    print("year" + "              " + "Date" + "                " + "Temp")
    print("--------------------------------------------")
    for key in weather_report:
        print(key, '\t\t', weather_report.get(key)['Min-Temp-date'], '\t\t',
              weather_report.get(key)['Min-TempC'])


if __name__ == '__main__':
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
       basic_weather_Report()
    elif Report_no == Report_number.hottestdayreport.value:
        hottest_day_of_each_year()
    elif Report_no == Report_number.coolestdayreport.value:
        coolest_day_of_each_year()
    else:
        print("No such report found /n"
              "select correct report number")

