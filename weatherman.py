import os
import csv
import glob
import argparse

import sys

from datetime import datetime

import operator


def prepare_data_for_report(data_dir):
    os.chdir(data_dir)
    evaluations = get_evaluation_header()

    value_key = "value"
    date_key = "date"

    data_dict = {}
    for weather_file in glob.glob('*.txt'):
        with open(weather_file, "r") as csvfile:
            # to ignore header line
            csvfile.readline()
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    try:
                        date = row["PKT"]
                    except KeyError:
                        date = row["PKST"]

                    year = datetime.strptime(str(date), "%Y-%m-%d").year

                    for evaluate in evaluations:
                        key_header = evaluate[0]
                        operation = evaluate[1]
                        temp = int(row[key_header])

                        if year not in data_dict:
                            data_dict[year] = {}
                        if key_header not in data_dict[year]:
                            data_dict[year][key_header] = {value_key: temp,
                                                           date_key: date}
                            continue

                        if operation(temp, data_dict[year][key_header][value_key]) \
                                or not data_dict[year][key_header][value_key]:
                            data_dict[year][key_header] = {value_key: temp,
                                                           date_key: date}

                except ValueError:
                    # need to find a good solution
                    # This occurs because of last line in file
                    continue

    # print(data_dict)
    return data_dict


def get_evaluation_header():
    max_temp = ["Max TemperatureC", operator.gt]
    min_temp = ["Min TemperatureC", operator.lt]
    max_humid = ["Max Humidity", operator.gt]
    min_humid = [" Min Humidity", operator.lt]

    evaluations = [
        max_temp,
        min_temp,
        max_humid,
        min_humid
    ]

    return evaluations


def print_report(data_dict, report_no):
    evaluations = get_evaluation_header()
    if report_no == 1:
        print("Annual Max/Min Temperature")
        print_annual_evaluations(evaluations, data_dict)
    elif report_no == 2:
        print("Hottest day of each year")
        annual_evaluation_day(data_dict, evaluations[0][0])
    elif report_no == 3:
        print("Coldest day of each year")
        annual_evaluation_day(data_dict, evaluations[1][0])


def print_annual_evaluations(evaluations, data_dict):
    print ('%s\t%s\t%s\t%s\t%s' % ("Year",
                                   evaluations[0][0],
                                   evaluations[1][0],
                                   evaluations[2][0],
                                   evaluations[3][0]))
    print (
    '------------------------------------------------------------------------------------------')
    for key_year, eval_dict in data_dict.items():
        print ('%s\t\t%s\t\t\t%s\t\t\t%s\t\t%s' % (
            str(key_year),
            eval_dict[evaluations[0][0]]["value"],
            eval_dict[evaluations[1][0]]["value"],
            eval_dict[evaluations[2][0]]["value"],
            eval_dict[evaluations[3][0]]["value"]))


def annual_evaluation_day(data_dict, evaluate):
    print ('%s\t\t%s\t\t\t\t%s' % ("Year", "Date", "Temp"))

    print ('------------------------------------------------------------')
    for key_year, eval_dict in data_dict.items():
        print ('%s\t\t%s\t\t\t%s' % (
            str(key_year),
            eval_dict[evaluate]["date"],
            eval_dict[evaluate]["value"]))


def valid(report_no=0, data_dir=''):
    try:
        val = int(report_no)
        if not val in range(1, 4):
            print("Enter integer between 1 - 3")
            return False
    except ValueError:
        print("Enter integer between 1 - 3")
        return False

    if not os.path.isdir(data_dir):
        print("Weather data directory does not exist")
        return False

    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "report_no",
        help="1 for Annual Max/Min Temperature "
             + "\n2 for Hottest day of each year "
             + "\n3 for coldest day of each year",
        type=int)
    parser.add_argument(
        "data_dir",
        help="Directory containing weather data files")
    args = parser.parse_args()

    if valid(args.report_no, args.data_dir):
        data_dict = prepare_data_for_report(args.data_dir)
        print_report(data_dict, args.report_no)


main()
