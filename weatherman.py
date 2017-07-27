import csv
import os
import collections
import argparse
from datetime import datetime


class Record:
    max_temperature = 0
    min_temperature = 100
    max_humidity = 0
    min_humidity = 500
    date = "00/00/00"


def update_record(month_max_t, month_min_t, month_max_h, month_min_h, record):
    """This function Updates the Yearly Record"""
    max_temp_date_index = -1
    if record.max_temperature < int(max(month_max_t)):
        record.max_temperature = int(max(month_max_t))
        max_temp_date_index = month_max_t.index(record.max_temperature)
    if record.min_temperature > int(min(month_min_t)):
        record.min_temperature = int(min(month_min_t))
    if record.max_humidity < int(max(month_max_h)):
        record.max_humidity = int(max(month_max_h))
    if record.min_humidity > int(min(month_min_h)):
        record.min_humidity = int(min(month_min_h))
    return record, max_temp_date_index


def application_usage_info():
    """Function to Display Help"""
    print("[Report #]\n1 for Annual Max/Min Temperature and Humidity\n2 for Hottest day of each year\n")
    print("[Data_dir]\nDirectory containing weather data files")


def process_month_data(month_data, yearly_record):
    """This function processes the available data"""
    monthly_max_temp = []
    monthly_min_temp = []
    monthly_max_hum = []
    monthly_min_hum = []
    max_temp_date = []
    for each_day_date in month_data:
        date = each_day_date['PKT'] if ('PKT' in each_day_date) else each_day_date['PKST']
        if each_day_date['Max TemperatureC'] != '':
            monthly_max_temp.append(int(each_day_date['Max TemperatureC']))
            max_temp_date.append(date)
        else:
            monthly_max_temp.append(0)
        if each_day_date['Min TemperatureC'] != '':
            monthly_min_temp.append(int(each_day_date['Min TemperatureC']))
        if each_day_date['Max Humidity'] != '':
            monthly_max_hum.append(int(each_day_date['Max Humidity']))
        if each_day_date[' Min Humidity'] != '':
            monthly_min_hum.append(int(each_day_date[' Min Humidity']))
    data_year = date[0:4]
    record = yearly_record[data_year]
    #  Storing Updated Record
    record, max_temp_date_index = update_record(monthly_max_temp, monthly_min_temp,
                                                monthly_max_hum, monthly_min_hum, record)
    #   Updating Date
    if not max_temp_date_index == -1:
        record.date = max_temp_date[max_temp_date_index]
        yearly_record[data_year] = record


def display_yearly_records(years_record):
    """Function to display record of each year"""
    ordered_data_over_years = collections.OrderedDict(sorted(years_record.items()))
    print("Year\tMAX Temp\tMIN Temp\tMAX Humidity\tMIN "
          "Humidity\n--------------------------------------------------------------\n")
    for year in ordered_data_over_years:
        print("%s\t%d\t\t%d\t\t%d\t\t%d\n" % (year, ordered_data_over_years[year].max_temperature,
                                              ordered_data_over_years[year].min_temperature,
                                              ordered_data_over_years[year].max_humidity,
                                              ordered_data_over_years[year].min_humidity))


def display_max_temp_yearly(years_record):
    """Function to display max temperatures of each year"""
    ordered_data_over_years = collections.OrderedDict(sorted(years_record.items()))
    print(
        "Year\t\tDate\t\tTemp\n--------------------------------------------\n"
    )
    for year in ordered_data_over_years:
        date = ordered_data_over_years[year].date.split("-")
        date = "{:%d/%m/%Y}".format(datetime(int(date[0]), int(date[1]), int(date[2])))
        print("%s\t\t%s\t%d\n" % (year, str(date), ordered_data_over_years[year].max_temperature))


def get_years_list_from_files(files):
    years = []
    for name in files:
        if name.endswith('.txt'):
            year_value = name.split('_')
            if year_value[2] not in years:
                years.append(year_value[2])
    return years


def process(data_files, report_type):
    years = get_years_list_from_files(data_files)
    years_record = dict((key, Record()) for key in years)
    for file in data_files:
        if file.endswith('.txt'):
            with open(report_type.dir + file, 'r') as csvfile:
                month_data = csv.DictReader(csvfile)
                process_month_data(month_data, years_record)
    if report_type.report == "a":
        display_yearly_records(years_record)
    elif report_type.report == "b":
        display_max_temp_yearly(years_record)


def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('report', nargs='?', const=1)
    parser.add_argument('dir', nargs='?', const=1)
    args = parser.parse_args()
    weather_files = os.listdir(args.dir)
    if (args.report is not None) and args.dir is not None:
        process(weather_files, args)
    else:
        application_usage_info()


if __name__ == "__main__":
    main()
