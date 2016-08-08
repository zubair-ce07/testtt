import os
import re
import csv
import argparse
from collections import namedtuple
from enum import Enum


class REPORT_NUMBER(Enum):
    basicweatherreport = 1
    hottestdayreport = 2
    coolestdayreport = 3
    mean_temperature_report = 4


def reading_and_processing_data(reader, stats, min_temps, min_hums, year):
    for row in reader:
        max_temp = row.get('Max TemperatureC')
        min_temp = row.get('Min TemperatureC')
        max_hum = row.get('Max Humidity')
        min_hum = row.get(' Min Humidity')
        row_date = row.get('PKT') or row.get('PKST')

        if min_hum:  # Adding minimum humidities in a list
            min_hums.append(min_hum)

        if min_temp:  # Adding minimum temperatures & dates in  minimum_temperatures_dictionary
            min_temps[row_date] = min_temp

        if max_temp:  # Calculating maximum temperature & respective date
            max_int = int(max_temp)
            if stats[year].maximum_temperature == 0:
                stats[year] = stats[year]._replace(maximum_temperature=max_int)
                stats[year] = stats[year]._replace(max_temp_date=row_date)
            elif stats[year].maximum_temperature < max_int:
                stats[year] = stats[year]._replace(maximum_temperature=max_int)
                stats[year] = stats[year]._replace(max_temp_date=row_date)

        if max_hum:  # Calculating maximum_humidity
            hum_int = int(max_hum)
            if stats[year].maximum_humidity == 0:
                stats[year] = stats[year]._replace(maximum_humidity=hum_int)
            elif stats[year].maximum_humidity < hum_int:
                stats[year] = stats[year]._replace(maximum_humidity=hum_int)

    '''Calculating minimum temperature of each year and
        respective date in following block of code'''

    min_date = ''
    min_hum_value = 0
    min_temp_value = 0
    if min_hums:
        min_hum_value = min(min_hums)
    if stats[year].minimum_humidity == 0:
        stats[year] = stats[year]._replace(minimum_humidity=min_hum_value)
    elif int(stats[year].minimum_humidity) > int(min_hum_value):
        stats[year] = stats[year]._replace(minimum_humidity=min_hum_value)

    if min_temps:
        min_temp_value = min(min_temps.values())
        min_date = min(min_temps, key=min_temps.get)

    if stats[year].minimum_temperature == 0:
        stats[year] = stats[year]._replace(minimum_temperature=min_temp_value)
        stats[year] = stats[year]._replace(min_temp_date=min_date)
    elif int(stats[year].minimum_temperature) > int(min_temp_value):
        stats[year] = stats[year]._replace(minimum_temperature=min_temp_value)
        stats[year] = stats[year]._replace(min_temp_date=min_date)

    return stats


'''
This function calculates all required parameters and
stores them in a dictionary & return in the end.
'''


def getting_weather_report(data_path):
    weatherman_report_data = {}
    stat1 = namedtuple('stat1',
                       'maximum_temperature minimum_temperature maximum_humidity minimum_humidity max_temp_date'
                       ' min_temp_date')
    year_stats = stat1(maximum_temperature=0, minimum_temperature=0, maximum_humidity=0, minimum_humidity=0,
                       max_temp_date='', min_temp_date='')
    for filename in os.listdir(data_path):
        file_path = os.path.join(data_path, filename)
        with open(file_path) as csvfile:
            name = csvfile.name
            year = (re.split('_', name))
            file_year = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            minimum_humidities = []  # To store 'Min Temperature' key values of a file.'''
            min_temp_and_date = {}
            ''' Above dictionary has a key date & minimum temperature
                on that day as value & datea of key values of a file.'''

            if file_year in weatherman_report_data:  # Updating values of existing key
                reading_and_processing_data(reader,
                                            weatherman_report_data, min_temp_and_date,
                                            minimum_humidities, file_year)

            else:  # Adding a new key
                weatherman_report_data[file_year] = year_stats
                reading_and_processing_data(reader,
                                            weatherman_report_data, min_temp_and_date,
                                            minimum_humidities, file_year)
    return weatherman_report_data


'''
This function basic_weather_report outputs formatted
report containg maximum temperature, minimum temperature,
maximum humidity & minimum humidity yearly.
'''


def yearly_weather_report(absolute_data_Path):
    weather_report = getting_weather_report(absolute_data_Path)
    print("Year" + "  " + "Maximum Temprature " + "  " + "Minimum Temprature" +
          "   " + "Maximum Humidity" + "   " + "Minimum Humidity")
    print("-----------------------------------------------------------------------------------")
    for key in weather_report:
        print('{0: <16} {1: <16} {2: <16} {3: <16} {4: <16}'.format(key, weather_report.get(key)[0],
                                                                    weather_report.get(key)[1],
                                                                    weather_report.get(key)[2],
                                                                    weather_report.get(key)[3]))


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
        print('{0: <16} {1: <16} {2: <16}'.format(key, weather_report.get(key)[4],
                                                  weather_report.get(key)[0]))


'''
This function outputs formatted report comtaing
minimum temperature & date of that day.
'''


def coolest_day_of_each_year(absolute_data_path):
    weather_report = getting_weather_report(absolute_data_path)
    print("This is report# 3")
    print("year"'\t\t' + "Date"'\t\t' "Temp")
    print("--------------------------------------------")
    for key in weather_report:
        print('{0: <16} {1: <16} {2: <16}'.format(key, weather_report.get(key)[5],
                                                  weather_report.get(key)[1]))


'''This function outputs average temprature of a given month of the year'''


def calculate_mean_temperature_of_month(data_path):
    month_ = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4',
              'May': '5', 'Jun': '6', 'Jul': '7', 'Aug': '8',
              'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    mean_sum = 0
    count = 0
    month_year = input("Enter month and year in mm-yy format : ")
    for file_ in os.listdir(data_path):
        file_path = os.path.join(data_path, file_)
        with open(file_path) as csvfile:
            name = csvfile.name
            filename_ = (re.split ('[_ .]', name))
            month_year_parsed = (re.split('-', month_year))
            for key in month_:
                if month_year_parsed[0] in month_[key]:
                    month_year_parsed[0] = key

            if month_year_parsed[0] in filename_ and month_year_parsed[1] in filename_:
                next(csvfile)
                reader = csv.DictReader(csvfile)
                for row in reader:
                    count = count + 1

                    mean_temp = row.get('Mean TemperatureC')
                    if mean_temp:
                        x = int(mean_temp)
                        mean_sum = mean_sum + x
    average = mean_sum / count
    print("Average temperature = ", average)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reportnumber", help="input the report number", type=int)
    parser.add_argument("weatherdatapath", help="input the path that contains data files")
    args = parser.parse_args()
    report_no = args.reportnumber
    weatherdata_path = args.weatherdatapath
    if os.path.exists(weatherdata_path):
        if report_no == REPORT_NUMBER.basicweatherreport.value:
            yearly_weather_report(weatherdata_path)
        elif report_no == REPORT_NUMBER.hottestdayreport.value:
            hottest_day_of_each_year(weatherdata_path)
        elif report_no == REPORT_NUMBER.coolestdayreport.value:
            coolest_day_of_each_year(weatherdata_path)
        elif report_no == REPORT_NUMBER.mean_temperature_report.value:
            calculate_mean_temperature_of_month(weatherdata_path)
        else:
            print("No such report found /n"
                  "select correct report number")


if __name__ == '__main__':
    main()

