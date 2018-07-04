import os
from weather import FileParser, WeatherDisplay, Calculator
import argparse


def validate_year(string):
    if len(string) == 4 and string.isdigit():
        return string
    else:
        raise TypeError


def validate_month(string):
    date_arg = string.split('/')

    if not len(date_arg) == 2:
        raise TypeError

    year_arg = date_arg[0]
    month_arg = date_arg[1]

    if len(year_arg) == 4 and len(month_arg) > 0 and year_arg.isdigit() and month_arg.isdigit():
        return string
    else:
        raise TypeError


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")

    parser.add_argument("-e", help=("For a given year display the highest temperature and day,"
                                    " lowest temperature and day, most humid day and humidity"),
                        action="append", type=validate_year)

    parser.add_argument("-a", help=("For a given month display the average highest temperature,"
                                    " average lowest temperature,average mean humidity"),
                        action="append", type=validate_month)

    parser.add_argument("-c",
                        help=("For a given month draw two horizontal bar charts on"
                              " the console for the highest and"
                              " lowest temperature on each day. Highest in red and lowest in blue"),
                        action="append", type=validate_month)

    parser.add_argument("-b", help=("For a given month draw one horizontal bar chart on the console"
                                    " for the highest and lowest temperature on each day."
                                    " Highest in red and lowest in blue."),
                        action="append", type=validate_month)
    return parser.parse_args()


def parse_date(date):
    date = date.split('/')
    year = date[0]
    month = date[1]

    month = str(int(month))
    return year, month


def calculate_results(args, weather_readings):
    calculator = Calculator()
    display = WeatherDisplay()

    for arg in args.a or []:
        year, month = parse_date(arg)
        result = calculator.calculate_monthly_average_report(weather_readings, year, month)
        display.present_monthly_average_report(result)

    for arg in args.b or []:
        year, month = parse_date(arg)
        result = calculator.calculate_daily_extremes_report(weather_readings, year, month)
        display.present_daily_extremes_report(result, horizontal=True)

    for arg in args.c or []:
        year, month = parse_date(arg)
        result = calculator.calculate_daily_extremes_report(weather_readings, year, month)
        display.present_daily_extremes_report(result)

    for arg in args.e or []:
        result = calculator.calculate_annual_result(weather_readings, year=arg)
        display.present_annual_report(result)


def main():
    arguments = get_arguments()

    if not os.path.exists(arguments.directory):
        print('Invalid Directory Path')
        return

    parser = FileParser()
    files = parser.get_files(arguments.directory)

    if len(files) == 0:
        print('No valid files found in directory')
        return

    weather_readings = parser.read(files)
    calculate_results(arguments, weather_readings)


if __name__ == "__main__":
    main()
