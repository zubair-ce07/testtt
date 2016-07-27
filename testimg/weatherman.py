import csv
import argparse
import os
import glob
import sys
from collections import namedtuple


def display_weather_stats(report_number, stats):
    """Displays the output of the report"""
    if (report_number == 1):
        print'{0} {1}'.format("This is report number: ", report_number)
        print("Year         MAX Temp         MIN Temp"
              "         MAX Humidity         MIN Humidity")
        print("----------------------------------------"
              "----------------------------------------")
        for each_year in stats:
            print('{0: <5}        {1: <5}               {2: <5}'
                  '               {3: <5}                   {4: <5}'
                  .format(each_year,
                          (stats[each_year]).max_temp,
                          (stats[each_year]).min_temp,
                          (stats[each_year]).max_humid,
                          (stats[each_year]).min_humid))
    elif (report_number == 2):
            print'{0} {1}'.format("This is report number: ", report_number)
            print("Year          Date                 Temp")
            print("---------------------------------------")
            for each_year in stats:
                print'{0: <5}        {1: <10}              {2: <5}'\
                    .format(each_year,
                            (stats[each_year]).date,
                            (stats[each_year]).max_temp)
    return


def min_or_max_key_value(list_of_dicts, key, min_or_max):
    """Function that returns the max value of a key from a list of dictionaries"""
    seq = [x[key] for x in list_of_dicts if x[key] != '']
    if (min_or_max == 'min'):
        return min(seq) if seq else '200'
    elif (min_or_max == 'max'):
        return max(seq) if seq else '-200'


def calculate_yearly_weather_report(month_data_parsed, year, stats):
    year_stats = namedtuple('year_stats',
                            ['max_temp', 'min_temp', 'max_humid', 'min_humid'])
    if year in stats:
        month_data_parsed.append({'Max TemperatureC': stats[year].max_temp,
                                  'Min TemperatureC': stats[year].min_temp,
                                  'Max Humidity': stats[year].max_humid,
                                  ' Min Humidity': stats[year].min_humid})
    min_temp = min_or_max_key_value(month_data_parsed, 'Min TemperatureC', 'min')
    max_temp = min_or_max_key_value(month_data_parsed, 'Max TemperatureC', 'max')
    min_humid = min_or_max_key_value(month_data_parsed, ' Min Humidity', 'min')
    max_humid = min_or_max_key_value(month_data_parsed, 'Max Humidity', 'max')
    stats[year] = year_stats(max_temp, min_temp, max_humid, min_humid)


def yearly_weather_report(files, stats):
    """function to generate report number 1: the max temperate, min temparature. max humidity and min humidity for every year"""
    for file_ in files:
        year = (int(filter(str.isdigit, file_)))
        with open(file_) as f:
            month_data = csv.DictReader(f)
            month_data_parsed = list(month_data)
            calculate_yearly_weather_report(month_data_parsed, year, stats)
    display_weather_stats(1, stats)
    return


def calculate_yearly_hottest_days(month_data_parsed, year, stats):
    year_stats = namedtuple('year_stats', ['date', 'max_temp'])
    if year in stats:
        month_data_parsed.append({'Max TemperatureC': stats[year].max_temp,
                                  'PKT': stats[year].date})
    row_of_max_temp = max(month_data_parsed, key=lambda x: x.get('Max TemperatureC'))
    max_temp = row_of_max_temp['Max TemperatureC']
    date = row_of_max_temp.get('PKT') or row_of_max_temp.get('PKST')
    stats[year] = year_stats(date, max_temp)
    return


def yearly_hottest_days_report(files, stats):
    """function to generate report number 2: hottest days of each year"""
    for file_ in files:
        year = (int(filter(str.isdigit, file_)))
        with open(file_) as f:
            month_data = csv.DictReader(f)
            month_data_parsed = list(month_data)
            calculate_yearly_hottest_days(month_data_parsed, year, stats)
    display_weather_stats(2, stats)
    return


def main():
    """Main function of this program"""
    parser = argparse.ArgumentParser()
    parser.add_argument("R", help="input the report number")
    parser.add_argument("filepath", help="input the path that contains data files")
    args = parser.parse_args()
    try:
        os.chdir(args.filepath)
        files_found = glob.glob("*.txt")
    except OSError:
        print("The directory path is not valid")
        sys.exit(1)
    report_num = int(args.R)
    stats = {}
    if (report_num == 1):
        yearly_weather_report(files_found, stats)
    elif (report_num == 2):
        yearly_hottest_days_report(files_found, stats)


if __name__ == "__main__":
    main()
