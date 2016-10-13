import sys
import os
import csv
import datetime
import argparse
import calendar
from operator import itemgetter, attrgetter


class WeatherMan:
    def __init__(self):
        return

    @staticmethod
    def clean_blank_in_dictionary(records_dictionary):
        records_dictionary = \
            dict((k, v) for k, v in records_dictionary.iteritems() if v)
        return records_dictionary

    @staticmethod
    def find_maximum_in_dictionary(temperature_records):
        dictionary_numeric_values = \
            list(map(int, temperature_records.values()))
        dictionary_max_value = max(dictionary_numeric_values)
        dictionary_keys = map(WeatherMan().parse_date,
                              [k for k, v in temperature_records.items()
                               if v == str(dictionary_max_value)])
        dictionary_max_key = max(dictionary_keys)
        return [dictionary_max_value, dictionary_max_key]

    @staticmethod
    def find_minimum_in_dictionary(temperature_records):
        dictionary_numeric_values = \
            list(map(int, temperature_records.values()))
        dictionary_min_value = min(dictionary_numeric_values)
        dictionary_keys = map(WeatherMan().parse_date,
                              [k for k, v in temperature_records.items()
                               if v == str(dictionary_min_value)])
        dictionary_min_key = min(dictionary_keys)
        return [dictionary_min_value, dictionary_min_key]

    @staticmethod
    def calculate_annual_report(temperature_records):
        daily_date_record = [x['PKT'] for x in temperature_records]

        daily_max_temperature_record = \
            [x['Max TemperatureC'] for x in temperature_records]
        temperature_date_dictionary = \
            dict(zip(daily_date_record, daily_max_temperature_record))
        temperature_date_dictionary = \
            WeatherMan().clean_blank_in_dictionary(temperature_date_dictionary)
        max_temperature_record =\
            WeatherMan().find_maximum_in_dictionary(temperature_date_dictionary)

        daily_min_temp_record = [x['Min TemperatureC'] for x in temperature_records]
        min_temperature_date_dictionary = \
            dict(zip(daily_date_record, daily_min_temp_record))
        min_temperature_date_dictionary = \
            WeatherMan().clean_blank_in_dictionary(min_temperature_date_dictionary)
        min_temperature_record = \
            WeatherMan().find_minimum_in_dictionary(min_temperature_date_dictionary)

        humidity_record = [x['Max Humidity'] for x in temperature_records]
        humidity_date_dictionary = \
            dict(zip(daily_date_record, humidity_record))
        humidity_date_dictionary = \
            WeatherMan().clean_blank_in_dictionary(humidity_date_dictionary)
        max_humidity_record = \
            WeatherMan().find_maximum_in_dictionary(humidity_date_dictionary)

        annual_report = []
        annual_report.append(max_temperature_record)
        annual_report.append(min_temperature_record)
        annual_report.append(max_humidity_record)
        return annual_report

    @staticmethod
    def print_annual_report(annual_report):
        max_temperature_record = annual_report[0]
        max_temperature_day = max_temperature_record[1].day
        max_temperature_month = month_of_year[max_temperature_record[1].month - 1]
        print ("Highest : " +
               str(max_temperature_record[0]) +
               " on " +
               str(max_temperature_day) +
               " " +
               str(max_temperature_month)
               )
        min_temperature_record = annual_report[1]
        min_temperature_day = min_temperature_record[1].day
        min_temperature_month = month_of_year[min_temperature_record[1].month - 1]
        print ("Lowest  : " +
               str(min_temperature_record[0]) +
               " on " +
               str(min_temperature_day) +
               " " +
               str(min_temperature_month)
               )
        max_humidity_record = annual_report[2]
        most_humid_day = max_humidity_record[1].day
        most_humid_month = month_of_year[max_humidity_record[1].month - 1]
        print("Max Humidity : " +
              str(max_humidity_record[0]) +
              " on " +
              str(most_humid_day) +
              " " +
              str(most_humid_month)
              )

    @staticmethod
    def calculate_monthly_report(temperature_records):
        daily_maximum_temperature = \
            [x['Max TemperatureC'] for x in temperature_records if x['Max TemperatureC']]
        maximum_temperature_mean = reduce(
            lambda x, y: x + y,
            map(int, daily_maximum_temperature)) / len(daily_maximum_temperature)

        daily_minimum_temperature = \
            [x['Min TemperatureC'] for x in temperature_records if x['Min TemperatureC']]
        mainimum_temperature_mean = reduce(
            lambda x, y: x + y,
            map(int, daily_minimum_temperature)) / len(daily_minimum_temperature)

        daily_mean_humidity = \
            [x['Mean Humidity'] for x in temperature_records if x['Mean Humidity']]
        maximum_humidity_mean = reduce(
            lambda x, y: x + y,
            map(int, daily_mean_humidity)) / len(daily_mean_humidity)

        monthly_mean_calculations = []
        monthly_mean_calculations.append(maximum_temperature_mean)
        monthly_mean_calculations.append(mainimum_temperature_mean)
        monthly_mean_calculations.append(maximum_humidity_mean)
        return monthly_mean_calculations

    @staticmethod
    def print_monthly_calcualtion(monthly_mean_calculations):
        highest_average = monthly_mean_calculations[0]
        lowest_average = monthly_mean_calculations[1]
        average_mean_humidity = monthly_mean_calculations[2]
        print ("Highest Average : " + 
               str(highest_average) + "C")
        print ("Lowest Average : " + 
               str(lowest_average) + "C")
        print ("Average Mean Humidity : " + 
               str(average_mean_humidity) + "%")

    @staticmethod
    def calculate_monthly_barchart_values(temperature_records):
        daily_calculation = []
        daily_maximum_temperatue = \
            [x['Max TemperatureC'] for x in temperature_records]
        daily_minimum_temperatue = \
            [x['Min TemperatureC'] for x in temperature_records]
        daily_calculation.append(daily_maximum_temperatue)
        daily_calculation.append(daily_minimum_temperatue)
        return daily_calculation

    @staticmethod
    def print_bar_chart(daily_calculation):
        column_to_be_read = [1, 3]
        color_start = ['\033[1;31m', '\033[1;34m']
        color_end = ['\033[1;m', '\033[1;m']
        for day in range(len(daily_calculation[0])):
            for iteration, column_number in enumerate(column_to_be_read):
                if daily_calculation[iteration][day]:
                    printline = '+' * int(daily_calculation[iteration][day])
                else:
                    printline = ""
                print (str(day + 1) +
                       color_start[iteration] +
                       printline +
                       color_end[iteration] +
                       daily_calculation[iteration][day]
                       )

    @staticmethod
    def calculate_oneline_chart_values(temperature_records):
        daily_maximum = [x['Max TemperatureC'] for x in temperature_records]
        daily_minimum = [x['Min TemperatureC'] for x in temperature_records]
        monthly_record = []
        monthly_record.append(daily_maximum)
        monthly_record.append(daily_minimum)
        return monthly_record

    @staticmethod
    def print_oneline_chart(monthly_record):
        daily_maximum = monthly_record[0]
        daily_minimum = monthly_record[1]
        red_color = ['\033[1;31m', '\033[1;m']
        blue_color = ['\033[1;34m', '\033[1;m']
        for day in range(len(daily_maximum)):
            if (daily_minimum[day]):
                bluebar = blue_color[0] + \
                          '+' * int(daily_minimum[day]) + \
                          blue_color[1]
            else:
                bluebar = ""
            if daily_maximum[day]:
                redbar = red_color[0] + \
                         '+' * int(daily_maximum[day]) \
                         + red_color[1]
            else:
                redbar = ""
            print (str(day + 1) +
                   bluebar + redbar +
                   daily_minimum[day] +
                   "-" +
                   daily_maximum[day])

    @staticmethod
    def read_csv_files(target_files):
        for file_for_processing in target_files:
            global header_attributes
            if os.path.isfile(file_for_processing):
                with open(file_for_processing, 'r') as csvfile:
                    next(csvfile)
                    file_reader = csv.DictReader(
                        filter(lambda row: row[0] != '<', csvfile)
                    )
                    file_reader.fieldnames[0] = "PKT"
                    file_reader.fieldnames[1] = "Max TemperatureC"
                    file_reader.fieldnames[3] = "Min TemperatureC"
                    file_reader.fieldnames[7] = "Max Humidity"
                    file_reader.fieldnames[8] = "Mean Humidity"
                    header_attributes = file_reader.fieldnames
                for line in file_reader:
                    temperature_records.append(line)
        return temperature_records

    @staticmethod
    def fetch_required_files(date_argument):
        year = date_argument[0]
        if len(date_argument) < 2:
            for filename in files_in_directory:
                if filename.__contains__(year) and filename:
                    file_prefix = argument.path_to_file + "/" + filename
                    target_files.append(file_prefix)
        else:
            if len(date_argument) > 1:
                month = date_argument[1]
                for filename in files_in_directory:
                    if (filename.__contains__(year) and
                            filename.__contains__(month_of_year[int(month) - 1])):
                        file_prefix = argument.path_to_file + "/" + filename
                        target_files.append(file_prefix)
        return target_files

    @staticmethod
    def parse_date(calculated_date):
        date = calculated_date.split("-")
        formated_date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        return formated_date


if __name__ == '__main__':
    month_of_year = [month for month in calendar.month_abbr]
    month_of_year.pop(0)
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--annual", action="store_true")
    group.add_argument("-a", "--monthly", action="store_true")
    group.add_argument("-c", "--bar_chart", action="store_true")
    group.add_argument("-c4", "--oneline_chart", action="store_true")
    parser.add_argument("report_date", help="Date")
    parser.add_argument("path_to_file", help="Path of folder")
    argument = parser.parse_args()
    files_in_directory = \
        [target_file for target_file in os.listdir(argument.path_to_file)]
    target_files = []
    date_argument = argument.report_date.split("/")
    target_files = \
        WeatherMan().fetch_required_files(date_argument)
    temperature_records = []
    temperature_records = \
        WeatherMan().read_csv_files(target_files)
    if argument.annual:
        annual_report = \
            WeatherMan().calculate_annual_report(temperature_records)
        WeatherMan().print_annual_report(annual_report)
    else:
        if argument.monthly:
            monthly_average_calculations = \
                WeatherMan().calculate_monthly_report(temperature_records)
            WeatherMan().print_monthly_calcualtion(monthly_average_calculations)
        else:
            if argument.bar_chart:
                monthly_maximum_calculations = \
                    WeatherMan().calculate_monthly_barchart_values(temperature_records)
                WeatherMan.print_bar_chart(monthly_maximum_calculations)
            else:
                if argument.oneline_chart:
                    monthly_maximum_calculations = \
                        WeatherMan().calculate_oneline_chart_values(temperature_records)
                    WeatherMan().print_oneline_chart(monthly_maximum_calculations)
