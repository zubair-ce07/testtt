import sys
import argparse

from parsing_class import ParsingFiles
from calculation_class import CalculatingResults
from report_class import ReportPrinting


def is_correct_input(input_data):
    for val in input_data:
        for alp in val:
            if str.isalpha(alp):
                return False
    return True


def parsing_arguments():
    argument_parser = argparse.ArgumentParser(add_help=False)
    argument_parser.add_argument('file_path')
    argument_parser.add_argument('-e', nargs='*')
    argument_parser.add_argument('-a', nargs='*')
    argument_parser.add_argument('-c', nargs='*')
    return argument_parser.parse_args()


if __name__ == "__main__":
    args = parsing_arguments()
    if args.e:
        year = args.e[0]
        if str.isnumeric(year):
            path = args.file_path
            flag = '-e'
            query = str(args.e[0])

            parsing_files = ParsingFiles(path, flag, query)
            all_weather_readings = parsing_files.reading_files()
            file_names = parsing_files.all_files_names

            calculations_class = CalculatingResults(all_weather_readings, file_names, flag)
            results = calculations_class.calculations()
            report_print = ReportPrinting(results, flag)
            report_print.print()
        else:
            print("\ninvalid input for -e!", args.e[0])

    if args.a:
        year_month = args.a[0].split('/')
        local_flag = is_correct_input(year_month)
        if local_flag:
            path = args.file_path
            flag = '-a'
            query = args.a[0]

            parsing_files = ParsingFiles(path, flag, query)
            all_weather_readings = parsing_files.reading_files()
            file_names = parsing_files.all_files_names

            calculations_class = CalculatingResults(all_weather_readings, file_names, flag)
            results = calculations_class.calculations()
            report_print = ReportPrinting(results, flag)
            report_print.print()
        else:
            print("\ninvalid input for -a!", args.a[0])

    if args.c:
        year_month = args.c[0].split('/')
        local_flag = is_correct_input(year_month)
        if local_flag:
            path = args.file_path
            flag = '-c'
            query = args.c[0]

            parsing_files = ParsingFiles(path, flag, query)
            all_weather_readings = parsing_files.reading_files()
            file_names = parsing_files.all_files_names

            calculations_class = CalculatingResults(all_weather_readings, file_names, flag)
            results = calculations_class.calculations()
            report_print = ReportPrinting(results, flag)
            report_print.print()
        else:
            print("\ninvalid input for -c!", args.c[0])