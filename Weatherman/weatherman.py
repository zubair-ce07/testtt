import argparse
import os
from datetime import datetime

from file_parser import FileParser
from report_generator import ReportGenerator
from result_calculations import ResultCalculations


def is_actual_dir(dirname):
    if os.path.isdir(dirname):
        return dirname

    msg = "{0} is not a directory".format(dirname)
    raise argparse.ArgumentTypeError(msg)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', type=is_actual_dir,
        help="Path to directory containing files (i.e weatherfiles/..)")
    parser.add_argument(
        '-e', type=lambda arg: datetime.strptime(arg, '%Y'),
        nargs="*", help="Enter the year (i.e 2002)")
    parser.add_argument(
        '-a', type=lambda arg: datetime.strptime(arg, '%Y/%m'),
        nargs="*", help="Enter the year/month (i.e 2011/03)")
    parser.add_argument(
        '-c', type=lambda arg: datetime.strptime(arg, '%Y/%m'),
        nargs="*", help="Enter the year/month (i.e 2011/03)")

    return parser.parse_args()


def main():
    arguments = parse_arguments()
    file_parser = FileParser()
    calculations = ResultCalculations()
    report = ReportGenerator()

    records = file_parser.read_all_weather_files(arguments.path)

    if arguments.e:
        for arg in arguments.e:
            report.generate_yearly_report(
                calculations.find_yearly_data(records, arg.year))

    if arguments.a:
        for arg in arguments.a:
            report.generate_monthly_report(
                calculations.calculate_average(records, arg.date()))

    if arguments.c:
        for arg in arguments.c:
            report.generate_graph(
                calculations.find_monthly_data(records, arg.date()))

if __name__ == "__main__":
    main()
