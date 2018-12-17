import glob
import csv
import datetime
import argparse
import calendar
import os

from colr import Colr

from temperature import Weather
import report


def read_file_data(f_name):
    single_month_data = []
    try:
        with open(f_name, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for splitted_line in csv_reader:
                date_portion_in_splitted_line = list(splitted_line.values())[0]
                splitted_date = date_portion_in_splitted_line.split('-')

                formatted_date = datetime.date(year=int(splitted_date[0]), month=int(splitted_date[1]),
                                               day=int(splitted_date[2]))

                max_temperature = splitted_line['Max TemperatureC']
                mean_temperature = splitted_line['Mean TemperatureC']
                min_temperature = splitted_line['Min TemperatureC']
                max_humidity = splitted_line['Max Humidity']
                mean_humidity = splitted_line[' Mean Humidity']
                min_humidity = splitted_line[' Min Humidity']

                temperature_object_ready_to_append = Weather(formatted_date, max_temperature, mean_temperature,
                                                             min_temperature, max_humidity, mean_humidity, min_humidity)
                single_month_data.append(temperature_object_ready_to_append)
            return single_month_data
    except FileNotFoundError as err:
            print(err)


def get_date(date, directory_path):
    str_month = ''
    abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    suplitted_date = date.split('/')
    year = int(suplitted_date[0])
    if len(suplitted_date) > 1:
        month = int(suplitted_date[1])
        for key, value in abbr_to_num.items():
            if month == value:
                str_month = key
                break
        file_list = glob.glob(f"{directory_path}*{repr(year)}?{str_month}.txt")
    else:
        file_list = glob.glob(f"{directory_path}*{repr(year)}?*.txt")

    if file_list:
        return file_list
    else:
        print(f"{Colr('File (', fore='red')}{year}_{str_month}{Colr(') Not Exist.', fore='red')}")


def main():
    parser = argparse.ArgumentParser()
    directory_path = ''
    parser.add_argument('path', type=str, help='Enter the path of the directory!')
    parser.add_argument('-e', '--date_for_year', type=str)
    parser.add_argument('-a', '--date_for_month', type=str)
    parser.add_argument('-c', '--date_for_month_for_same_color', type=str)
    parser.add_argument('-d', '--date_for_month_for_different_color', type=str)
    args = parser.parse_args()

    if os.path.isdir(args.path):
        directory_path = args.path
    else:
        print(f"{Colr('Directory (', fore='red')}{args.path}{Colr(') Not Exist!', fore='red')}")

    if args.date_for_year:
        year_data = []
        file_list = get_date(args.date_for_year[0], directory_path)
        if file_list:
            for file_name in file_list:
                year_data.append(read_file_data(file_name))
            report.yearly_lowest_highest_values(year_data)

    if args.date_for_month:
        file_list = get_date(args.date_for_month, directory_path)
        if file_list:
            data = read_file_data(file_list[0])
            report.monthly_average_values(data)

    if args.date_for_month_for_same_color:
        file_list = get_date(args.date_for_month_for_same_color, directory_path)
        if file_list:
            data = read_file_data(file_list[0])
            report.horizontal_bar_for_given_month(data)

    if args.date_for_month_for_different_color:
        file_list = get_date(args.date_for_month_for_different_color, directory_path)
        if file_list:
            data = read_file_data(file_list[0])
            report.mixed_bar_for_given_month(data)


if __name__ == '__main__':
    main()
