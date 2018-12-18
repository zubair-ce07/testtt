import glob
import csv
import datetime
import argparse
import os


from temperature import Weather
import report

RED = '\033[31m'
BLUE = '\033[34m'
RESET = '\033[0m'


def read_weather_data(file_list):
    weather_data = []
    for file_name in file_list:
        try:
            with open(file_name, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for line in csv_reader:
                    formatted_date = datetime.datetime.strptime(list(line.values())[0], '%Y-%m-%d')

                    max_temperature = line['Max TemperatureC']
                    mean_temperature = line['Mean TemperatureC']
                    min_temperature = line['Min TemperatureC']
                    max_humidity = line['Max Humidity']
                    mean_humidity = line[' Mean Humidity']
                    min_humidity = line[' Min Humidity']

                    weather = Weather(formatted_date, max_temperature, mean_temperature, min_temperature, max_humidity,
                                      mean_humidity, min_humidity)
                    weather_data.append(weather)
        except FileNotFoundError as err:
                print(err)
    return weather_data


def month_weather_file(month_date, directory_path):
    year = month_date.year
    month = datetime.datetime.strftime(month_date, '%b')
    file_list = glob.glob(f"{directory_path}*{repr(year)}?{month}.txt")
    try:
        if file_list:
            return file_list
        else:
            raise ValueError(f"'File ( {RED}{year}_{month} {RESET}') Not Found.")
    except ValueError as ve:
        print(ve)


def year_weather_file(year_date, directory_path):
    year = year_date.year
    file_list = glob.glob(f"{directory_path}*{repr(year)}?*.txt")
    if file_list:
        return file_list
    else:
        raise ValueError(f"{RED}File ({RESET}{year}{RED}){RESET} Not Exist!")


def valid_directory(path):
    try:
        if os.path.isdir(path):
            return path
        else:
            raise ValueError(f"{RED}Invalid Directory ({RESET}{path}{RED}){RESET}")
    except ValueError as ve:
        print(ve)


def valid_year(year_date):
    try:
        return datetime.datetime.strptime(year_date, '%Y')
    except ValueError:
        print(f"{RED}Invalid Year ({RESET}{year_date}{RED}){RESET}")


def valid_month(month_date):
    try:
        return datetime.datetime.strptime(month_date, '%Y/%m')
    except ValueError:
        print(f"{RED}Invalid month ({RESET}{month_date}{RED}){RESET}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=valid_directory, help='Enter the path of the directory!')
    parser.add_argument('-e', '--year_date', type=valid_year)
    parser.add_argument('-a', '--month_date', type=valid_month)
    parser.add_argument('-c', '--month_date_same_color', type=valid_month)
    parser.add_argument('-d', '--month_date_diff_color', type=valid_month)
    args = parser.parse_args()

    if args.year_date:
        file_list = year_weather_file(args.year_date, args.path)
        year_weather_data = read_weather_data(file_list)
        report.year_peak_values(year_weather_data)

    if args.month_date:
        file_list = month_weather_file(args.month_date, args.path)
        month_weather_data = read_weather_data(file_list)
        report.month_average_values(month_weather_data)

    if args.month_date_same_color:
        file_list = month_weather_file(args.month_date_same_color, args.path)
        month_weather_data = read_weather_data(file_list)
        report.bar_chart_same_color(month_weather_data)

    if args.month_date_diff_color:
        file_list = month_weather_file(args.month_date_diff_color, args.path)
        month_weather_data = read_weather_data(file_list)
        report.bar_chart_diff_color(month_weather_data)


if __name__ == '__main__':
    main()

