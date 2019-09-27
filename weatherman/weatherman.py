import argparse

from FilesParser import FilesParser
from CalculateResults import Results
from Reports import Report


def process_yearly_temperatures(path, year):
    f_parser = FilesParser()
    result_calculator = Results()
    results = Report()
    readings = f_parser.populate_temperatures(path, year)
    final_result = result_calculator.Calculate_yearly_results(readings)
    results.show_yearly_results(final_result)


def process_monthly_avgs(path, month):
    f_parser = FilesParser()
    result_calculator = Results()
    results = Report()
    temp_readings = f_parser.populate_temperatures(path, month)
    avg_result = result_calculator.calculate_avg(temp_readings)
    results.show_monthly_avgs(avg_result)


def process_monthly_temperatures(path, month):
    f_parser = FilesParser()
    temp_readings = f_parser.populate_temperatures(path, month)
    results = Report()
    results.show_monthly_temps(temp_readings, False)


def process_monthly_temps_bonus(path, month):
    f_parser = FilesParser()
    temp_readings = f_parser.populate_temperatures(path, month)
    results = Report()
    results.show_monthly_temps(temp_readings, True)


def arg_parser():
    arguments = argparse.ArgumentParser(description='Arguments for weatherman.py')
    arguments.add_argument('Path', metavar='path', type=str, help='the path to the files')
    arguments.add_argument('-e', help='Display Highest, Lowest temperatures and most humid day of given year')
    arguments.add_argument('-a', help='Average highest and lowest temps for given month')
    arguments.add_argument('-c', help='Display bars of temps of warmest and coldest days of given month')
    arguments.add_argument('-d', help='[BONUS] Display bars of temps of warmest and coldest days of given month')
    return arguments.parse_args()


if __name__ == "__main__":
    args = arg_parser()
    if args.e:
        process_yearly_temperatures(args.Path, args.e)

    if args.a:
        process_monthly_avgs(args.Path, args.a)

    if args.c:
        process_monthly_temperatures(args.Path, args.c)

    if args.d:
        process_monthly_temps_bonus(args.Path, args.d)
