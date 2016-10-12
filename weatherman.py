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
    def generate_annual_report(temperature_records):
        column_to_be_calculated = [1, 3, 7]
        value_to_be_printed = ["Highest : ", "Lowest : ", "Max Humidity : "]
        units = ["C", "C", "%"]
        calculated_value = 0

        for iteration, header_value in enumerate(column_to_be_calculated):
            calculated_date = ""
            daily_date_record = \
                [x[header_attributes[0]] for x in temperature_records]
            daily_record = \
                [x[header_attributes[header_value]] for x in temperature_records]

            if iteration == 1:
                daily_formated_record = \
                    [calculated_value if x == '' else x for x in daily_record]
                temp_date_dict = dict(
                    zip(daily_date_record, map(int, daily_formated_record)))
                calculated_value = min(temp_date_dict.values())
                calculated_date = min(temp_date_dict, key=temp_date_dict.get)
                calculation_date = WeatherMan().parse_date(calculated_date)
            else:
                daily_formated_record = \
                    [0 if x == '' else x for x in daily_record]
                temp_date_dict = dict(
                    zip(daily_date_record, map(int, daily_formated_record))
                )
                calculated_value = max(temp_date_dict.values())
                calculated_date = \
                    [k for k, v in temp_date_dict.items()
                     if v == calculated_value][-1]
                calculation_date = WeatherMan().parse_date(calculated_date)
            print (value_to_be_printed[iteration] +
                   str(calculated_value) +
                   units[iteration] +
                   " on " +
                   str(month_of_year[calculation_date.month - 1]) +
                   " " + str(calculation_date.day))

    @staticmethod
    def generate_monthly_report(temperature_records):
        column_to_be_calculated = [1, 3, 8]
        value_to_be_printed = ["Highest Average : ",
                               "Lowest Average : ",
                               "Average Mean Humidity : "]
        units = ["C", "C", "%"]
        for iteration, header_value in enumerate(column_to_be_calculated):
            daily_calculation = \
                [x[header_attributes[header_value]] for x in temperature_records]
            daily_formated_record = \
                [0 if x == '' else x for x in daily_calculation]
            mean_value = reduce(
                lambda x, y: x + y,
                map(int, daily_formated_record)) / len(daily_formated_record)
            print (value_to_be_printed[iteration] +
                   str(mean_value) + units[iteration])

    @staticmethod
    def generate_monthly_bar_chart(temperature_records):
        column_to_be_read = [1, 3]
        color_start = ['\033[1;31m', '\033[1;34m']
        color_end = ['\033[1;m', '\033[1;m']
        daily_calculation = []
        daily_calculation.append(
            [x[header_attributes[1]] for x in temperature_records]
        )
        daily_calculation.append(
            [x[header_attributes[3]] for x in temperature_records]
        )

        for day in range(len(temperature_records)):
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
    def generate_monthly_oneline_chart(temperature_records):
        red_color = ['\033[1;31m', '\033[1;m']
        blue_color = ['\033[1;34m', '\033[1;m']
        daily_calculation = []
        daily_maximum = [x[header_attributes[1]] for x in temperature_records]
        daily_minimum = [x[header_attributes[3]] for x in temperature_records]

        for day in range(len(temperature_records)):
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
                    header_attributes=file_reader.fieldnames
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
    files_in_directory = [target_file for target_file in os.listdir(argument.path_to_file)]
    target_files = []
    date_argument = argument.report_date.split("/")
    target_files = WeatherMan().fetch_required_files(date_argument)
    temperature_records = []
    temperature_records = WeatherMan().read_csv_files(target_files)
    if argument.annual:
        WeatherMan().generate_annual_report(temperature_records)
    else:
        if argument.monthly:
            WeatherMan().generate_monthly_report(temperature_records)
        else:
            if argument.bar_chart:
                WeatherMan().generate_monthly_bar_chart(temperature_records)
            else:
                if argument.oneline_chart:
                    WeatherMan().generate_monthly_oneline_chart(temperature_records)
