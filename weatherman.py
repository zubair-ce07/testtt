import argparse
import calendar

from parsing_class import ParsingFiles
from calculation_class import CalculatingResults
from report_class import ReportPrinting


def is_valid_year(year):
    if year and year.isdigit():
        if (int(year) >= 1900) and (int(year) <= 2020):
            return True
    return False


def is_valid_month(month):
    if month and month.isdigit():
        if (int(month) >= 1) and (int(month) <= 12):
            return True
    return False


def parsing_arguments():
    argument_parser = argparse.ArgumentParser(add_help=False)
    argument_parser.add_argument('file_path', type=str, help='Path to the weatherdata files directory.',
                                 default='/home/muhammad/new_task/weatherdata/')
    argument_parser.add_argument('-e', nargs='*', type=int, help='Enter year to print the results for that year.',
                                 default=[2000])
    argument_parser.add_argument('-a', nargs='*', type=str, help='Enter year/month in this format.', default=['2000/1'])
    argument_parser.add_argument('-c', nargs='*', type=str, help='Enter year/month in this format.', default=['2000/1'])
    return argument_parser.parse_args()


def append_year_month(argument_list, year_month):
    if is_valid_month(year_month[1]) and is_valid_year(year_month[0]):
        if year_month[0] not in argument_list:
            year_month[1] = calendar.month_abbr[int(year_month[1])]
            argument_list.append('_'.join(year_month))


def get_distinct_arguments_in_list(args):
    argument_list = []

    for arg_e in args.e:
        if is_valid_year(str(arg_e)):
            argument_list.append(str(arg_e))
        else:
            print("Invalid Input for arg -e !", arg_e)

    for arg_a in args.a:
        append_year_month(argument_list, arg_a.split('/'))

    for arg_c in args.c:
        append_year_month(argument_list, arg_c.split('/'))

    return argument_list


if __name__ == "__main__":
    args = parsing_arguments()
    argument_list = get_distinct_arguments_in_list(args)

    parsing_files = ParsingFiles(args.file_path, argument_list)
    all_weather_readings = parsing_files.reading_files()
    file_names = [file_name.replace('.txt', '') for file_name in parsing_files.all_files_names]

    calculations_class = CalculatingResults(all_weather_readings, file_names)
    calculations_class.calculations()
    results = calculations_class.results

    report_printer = ReportPrinting(results, args)
    report_printer.printing()

