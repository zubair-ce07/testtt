import glob
import csv
import datetime
import argparse
from colr import Colr as C

from temperature import Weather
import report

file_record = []


def read_monthly_file_data(f_name):
    single_month_data = []
    try:
        with open(f_name, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for splitted_line in csv_reader:
                date_portion_in_splitted_line = list(splitted_line.values())[0]
                splitted_date = date_portion_in_splitted_line.split('-')

                formatted_date = datetime.date(year=int(splitted_date[0]), month=int(splitted_date[1]), day=int(splitted_date[2]))

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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=str, help='Enter the path of the directory for weather data!')
    parser.add_argument('-e', '--date_for_year', type=str)
    parser.add_argument('-a', '--date_for_month', type=str)
    parser.add_argument('-c', '--date_for_month_for_same_color', type=str)
    parser.add_argument('-d', '--date_for_month_for_different_color', type=str)

    parsed_argumnets = parser.parse_args()

    directory_path = parsed_argumnets.path

    if parsed_argumnets.date_for_year:
        this_year_data_list = []
        suplitted_date = parsed_argumnets.date_for_year.split('/')
        year = int(suplitted_date[0])
        file_list = glob.glob(f"{directory_path}*{repr(year)}?*.txt")

        if file_list:
            for file_name in file_list:
                this_year_data_list.append(read_monthly_file_data(file_name))
            report.yearly_lowest_highest_values(this_year_data_list)
        else:
            print(f"{C('File (', fore='red')}{year}{C(') Does Not Exist....!', fore='red')}")

    if parsed_argumnets.date_for_month:
        this_year_data_list = []
        suplitted_date = parsed_argumnets.date_for_month.split('/')
        year = int(suplitted_date[0])
        month = int(suplitted_date[1])
        file_list = glob.glob(f"{directory_path}*{repr(year)}?*.txt")
        if file_list:
            for file_name in file_list:
                this_year_data_list.append(read_monthly_file_data(file_name))
            report.monthly_average_values(month, this_year_data_list)
        else:
            print(f"{C('File (', fore='red')}{year}_{month}{C(') Does Not Exist....!', fore='red')}")

    if parsed_argumnets.date_for_month_for_same_color:
        this_year_data_list = []
        suplitted_date = parsed_argumnets.date_for_month_for_same_color.split('/')
        year = int(suplitted_date[0])
        month = int(suplitted_date[1])

        file_list = glob.glob(f"{directory_path}*{repr(year)}?*.txt")
        if file_list:
            for file_name in file_list:
                this_year_data_list.append(read_monthly_file_data(file_name))
            report.horizontal_bar_for_given_month(month, this_year_data_list)
        else:
            print(f"{C('File (', fore='red')}{year}_{month}.txt{C(') Does Not Exist....!', fore='red')}")

    if parsed_argumnets.date_for_month_for_different_color:
        this_year_data_list = []
        suplitted_date = parsed_argumnets.date_for_month_for_different_color.split('/')
        year = int(suplitted_date[0])
        month = int(suplitted_date[1])
        file_list = glob.glob(f"{directory_path}*{repr(year)}?*.txt")
        if file_list:
            for file_name in file_list:
                this_year_data_list.append(read_monthly_file_data(file_name))
            report.mixed_bar_for_given_month(month, this_year_data_list)
        else:
            print(f"{C('File (', fore='red')}{year}_{month}.txt{C(') Does Not Exist....!', fore='red')}")


if __name__ == '__main__':
    main()
