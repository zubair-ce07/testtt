import glob
import csv
import datetime
import argparse
import os

from temperature import Weather
import calculation
import report

RED = '\033[31m'
BLUE = '\033[34m'
RESET = '\033[0m'


def read_weather_data(files_record):
    weather_data = []
    for file_name in files_record:
        try:
            with open(file_name, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for line in csv_reader:
                    formatted_date = datetime.datetime.strptime(list(line.values())[0], '%Y-%m-%d')

                    if is_valid(line):
                        max_temperature = line['Max TemperatureC']
                        mean_temperature = line['Mean TemperatureC']
                        min_temperature = line['Min TemperatureC']
                        max_humidity = line['Max Humidity']
                        mean_humidity = line[' Mean Humidity']
                        min_humidity = line[' Min Humidity']

                        weather = Weather(formatted_date, max_temperature, mean_temperature, min_temperature,
                                          max_humidity, mean_humidity, min_humidity)
                        weather_data.append(weather)
        except FileNotFoundError as err:
                print(err)
    return weather_data


def is_valid(line):
    validation_fields = ['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC', 'Max Humidity',
                         ' Mean Humidity', ' Min Humidity']
    return all([line[field] for field in validation_fields])


def weather_record(month_date, directory_path):
    year = month_date.year
    if datetime.datetime.strftime(month_date, '%b'):
        month = datetime.datetime.strftime(month_date, '%b')
        files_record = glob.glob(f"{directory_path}*{repr(year)}?{month}.txt")
    else:
        files_record = glob.glob(f"{directory_path}*{repr(year)}?*.txt")
    try:
        if files_record:
            return files_record
        else:
            raise ValueError(f"{RED}Record Not Found{RESET}")
    except ValueError as ve:
        print(ve)


def valid_directory(path):
    try:
        if os.path.isdir(path):
            return path
        else:
            raise ValueError(f"{RED}Invalid Directory ({RESET}{path}{RED}){RESET}")
    except ValueError as error:
        print(error)


def valid_year(year_date):
    try:
        return datetime.datetime.strptime(year_date, '%Y')
    except ValueError:
        print(f"{RED}Invalid date {RESET}")


def valid_month(month_date):
    try:
        print(datetime.datetime.strptime(month_date, '%Y/%m'))
        return datetime.datetime.strptime(month_date, '%Y/%m')
    except ValueError:
        print(f"{RED}Invalid date{RESET}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=valid_directory, help='Enter path of the directory!')
    parser.add_argument('-e', type=valid_year)
    parser.add_argument('-a', type=valid_month)
    parser.add_argument('-c', type=valid_month)
    parser.add_argument('-d', type=valid_month)
    args = parser.parse_args()

    if args.e:
        files_record = weather_record(args.e, args.path)
        year_weather_data = read_weather_data(files_record)
        calculated_data = calculation.year_peak_calculation(year_weather_data)
        report.year_peak_report(calculated_data)

    if args.a:
        files_record = weather_record(args.a, args.path)
        month_weather_data = read_weather_data(files_record)
        calculated_data = calculation.month_average_calculation(month_weather_data)
        report.month_average_report(calculated_data)

    if args.c:
        files_record = weather_record(args.c, args.path)
        month_weather_data = read_weather_data(files_record)
        calculated_data = calculation.month_peak_calculation(month_weather_data)
        report.bar_chart_report(calculated_data)

    if args.d:
        files_record = weather_record(args.d, args.path)
        month_weather_data = read_weather_data(files_record)
        calculated_data = calculation.month_peak_calculation(month_weather_data)
        report.bar_chart_report_bonus(calculated_data)


if __name__ == '__main__':
    main()

