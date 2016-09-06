import csv
import os
import sys
import argparse
import re
from enum import Enum
from operator import attrgetter


class Report_Number(Enum):
    yearly_weather_report = 1
    hottest_day_report = 2
    coolest_day_report = 3
    mean_temperature_report = 4


class Weather_Data:
    # Initializing class members of a weather_data instance
    def __init__(self, max_temp, min_temp, max_hum, min_hum, mean_temp, row_date):
        self.maximum_temperature = max_temp
        self.minimum_temperature = min_temp
        self.maximum_humidity = max_hum
        self.minimum_humidity = min_hum
        self.mean_temperature = mean_temp
        self.date_ = row_date

'''
This functon outputs yearly weather report,
containing maximum temperature, minimum temperature,
maximum humidity& minimum humidity.
'''

def get_yearly_weather_report(stats):
    year_report = {}
    for year in stats:      #iterating through every key
        temp_stats = stats[year]
        display_stats = []

        max_temp_year = max(map(attrgetter('maximum_temperature'), temp_stats))   #calculating yearly maximum temperature
        display_stats.append(max_temp_year)
        min_temp_year = min(map(attrgetter('minimum_temperature'), temp_stats))  #calculating yearly minimum temperature
        display_stats.append(min_temp_year)
        max_hum_year = max(map(attrgetter('maximum_temperature'), temp_stats))   #calculating yearly maximum humidity
        display_stats.append(max_hum_year)
        min_hum_year = min(map(attrgetter('minimum_temperature'), temp_stats))   #calculating yearly minimum humidity
        display_stats.append(min_hum_year)

        year_report[year] = display_stats

    print("This is report# 1")
    print("Year" + "  " + "Maximum Temperature " + "  " + "Minimum Temperature" +
              "   " + "Maximum Humidity" + "   " + "Minimum Humidity")
    print("-----------------------------------------------------------------------------------------")

    for key in sorted(year_report):
        print('{0: <16} {1: <16} {2: <16} {3: <16} {4: <16}'.format(key, year_report.get(key)[0],
                                                                    year_report.get(key)[1], year_report.get(key)[2],
                                                                    year_report.get(key)[3]))
'''
This function returns information regarding
hottest day of ech year.
'''


def get_hottest_day_report(stats):
    max_temp_records = {}

    for year in stats:          #iterating through every key
        temp_records = []
        temp_stats = stats[year]

        # Sorting list according to maximum temperature
        temp_stats.sort(key=lambda x: x.maximum_temperature, reverse=True)

        temp_records.append(str(temp_stats[0].date_))
        temp_records.append(str(temp_stats[0].maximum_temperature))
        max_temp_records[year] = temp_records

    print("This is report# 2")
    print("year" '\t\t'"Date"'\t\t'"Temp")
    print("--------------------------------------------")
    for key in sorted(max_temp_records):
        print('{0: <16} {1: <16} {2: <16}'.format(key, max_temp_records.get(key)[0],
                                                  max_temp_records.get(key)[1]))


'''
This function returns information regarding
coolest day of ech year.
'''

def get_coolest_day_report(stats):
    min_temp_records = {}
    for year in stats:          #iterating over years

        temp_stats = stats[year]     # getting list against year from dictionary
        temp_records = []

        # Sorting list according to mainimum temperature
        temp_stats.sort(key=lambda x: x.minimum_temperature, reverse=False)
        temp_records.append(str(temp_stats[0].date_))
        temp_records.append(str(temp_stats[0].minimum_temperature))
        min_temp_records[year] = temp_records
    print("This is report# 3")
    print("year" '\t\t'"Date"'\t\t'"Temp")
    print("--------------------------------------------")
    for key in sorted(min_temp_records):
        print('{0: <16} {1: <16} {2: <16}'.format(key, min_temp_records.get(key)[0],
                                                  min_temp_records.get(key)[1]))


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
            filename_ = (re.split('[_ .]', name))
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


'''This function collect all record objects from a file'''


def get_records_from_file(reader):

    # intializng a record
    file_records = []

    w = Weather_Data(0, 0, 0, 0, 0, '')
    for row in reader:
        if row.get('Max TemperatureC'):
            max_temp = int(row.get('Max TemperatureC'))
            w.maximum_temperature = max_temp
        if row.get('Min TemperatureC'):
            min_temp = int(row.get('Min TemperatureC'))
            w.minimum_temperature = min_temp
        if row.get('Max Humidity'):
            max_hum = int(row.get('Max Humidity'))
            w.maximum_humidity = max_hum
        if row.get(' Min Humidity'):
            min_hum = int(row.get(' Min Humidity'))
            w.minimum_humidity = min_hum
        if row.get('Mean TemperatureC'):
            mean_temp = int(row.get('Mean TemperatureC'))
            w.mean_temperature = mean_temp
        rowdate = row.get('PKT') or row.get('PKST')
        w.date_ = rowdate
        if w:
            file_records.append(w)
    return file_records


'''This function gathers all all record objects related to
a year and stores them as key(year)-values in a dictionary'''

def get_yearly_records(data_path, yearly_records):
    for file_ in os.listdir(data_path):
        if file_.find("_") is -1:
            print("File in given directory doesnt seems right ")
            sys.exit()
        tokens = file_.split("_")
        year = tokens[2]

        file_path = os.path.join(data_path, file_)

        with open(file_path) as csvfile:
            lines = csvfile.readlines()[1:-1]
            temp_list = []
            reader = csv.DictReader(lines)

            if year in yearly_records:
                temp_list = yearly_records[year]
                temp_list.extend(get_records_from_file(reader))
                yearly_records[year] = temp_list
            else:
                yearly_records[year] = temp_list
                temp_list.extend(get_records_from_file(reader))
                yearly_records[year] = temp_list

    return yearly_records



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reportnumber", help="input the report number", type=int)
    parser.add_argument("weatherdatapath", help="input the path that contains data files")
    args = parser.parse_args()
    report_no = args.reportnumber
    weatherdata_path = args.weatherdatapath
    stats = {}
    if os.path.exists(weatherdata_path):
        if report_no == Report_Number.yearly_weather_report.value:
            temp_stats = get_yearly_records(weatherdata_path, stats)
            get_yearly_weather_report(temp_stats)
        elif report_no == Report_Number.hottest_day_report.value:
            temp_stats = get_yearly_records(weatherdata_path, stats)
            get_hottest_day_report(temp_stats)
        elif report_no == Report_Number.coolest_day_report.value:
            temp_stats = get_yearly_records(weatherdata_path, stats)
            get_coolest_day_report(temp_stats)
        elif report_no == Report_Number.mean_temperature_report.value:
            calculate_mean_temperature_of_month(weatherdata_path)
        else:
            print("No such report found /n"
                  "select correct report number")

if __name__ == '__main__':
    main()

