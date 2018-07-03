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


def display_results(problem_type, result):
    display = WeatherDisplay()

    while len(problem_type):
        m = problem_type.pop()
        r = result.pop()

        print(m)
        if m == '-e':
            display.present_annual_report(r)
        elif m == '-a':
            display.present_monthly_average_report(r)
        elif m == '-b':
            display.present_daily_extremes_report(r, horizontal=True)
        elif m == '-c':
            display.present_daily_extremes_report(r)


def parse_date(date):
    date = date.split('/')
    year = date[0]
    month = date[1]

    month = str(int(month))
    return year, month


def calculate_results(args, weather_readings):
    calculator = Calculator()
    problem_type = []
    result = []

    for arg in args.a or []:
        year, month = parse_date(arg)
        problem_type.append('-a')
        result.append(calculator.calculate_monthly_average_report(weather_readings, year, month))

    for arg in args.b or []:
        year, month = parse_date(arg)
        problem_type.append('-b')
        result.append(calculator.calculate_daily_extremes_report(weather_readings, year, month))

    for arg in args.c or []:
        year, month = parse_date(arg)
        problem_type.append('-c')
        result.append(calculator.calculate_daily_extremes_report(weather_readings, year, month))

    for arg in args.e or []:
        problem_type.append('-e')
        result.append(calculator.calculate_annual_result(weather_readings, year=arg))

    return problem_type, result


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
    problem_type, result = calculate_results(arguments, weather_readings)

    problem_type.reverse()
    result.reverse()

    display_results(problem_type, result)


if __name__ == "__main__":
    main()
