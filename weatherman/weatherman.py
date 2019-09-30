import argparse

from CalculateResults import Results
from Reports import Report


def arg_parser():
    arguments = argparse.ArgumentParser(description='Arguments for weatherman.py')
    arguments.add_argument('Path', metavar='path', type=str, help='the path to the files')
    arguments.add_argument('-e', help='Display Highest, Lowest temperatures and most humid day of given year')
    arguments.add_argument('-a', help='Average highest and lowest temps for given month')
    arguments.add_argument('-c', help='Display bars of temps of warmest and coldest days of given month')
    arguments.add_argument('-d', help='[BONUS] Display bars of temps of warmest and coldest days of given month')
    return arguments.parse_args()


def main():
    args = arg_parser()
    result_calculator = Results()
    temperature_readings = result_calculator.parse_files(args.Path)
    show_results = Report()
    if args.e:
        yearly_temperatures_results = result_calculator.calculate_yearly_results(temperature_readings, args.e)
        show_results.show_yearly_results(yearly_temperatures_results)

    if args.a:
        monthly_avg_result = result_calculator.calculate_avg(temperature_readings, args.a)
        show_results.show_monthly_avgs(monthly_avg_result)

    if args.c:
        show_results.show_monthly_temps(temperature_readings, args.c, False)

    if args.d:
        show_results.show_monthly_temps(temperature_readings, args.c, True)


if __name__ == "__main__":
    main()
