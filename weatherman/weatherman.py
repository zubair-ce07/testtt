import argparse
import calendar
import datetime


from parsing_class import ParsingFiles
from calculation_class import CalculatingResults
from report_class import ReportPrinting


def valid_date(year, month=1, day=1):
    """This function is checking validation of date"""

    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        return False
    return True


def parsing_arguments():
    """This function is parsing argument"""

    argument_parser = argparse.ArgumentParser(add_help=False)
    argument_parser.add_argument('file_path', type=str, help='Path to the weatherdata files directory.',
                                 default='/home/muhammad/training-tasks/the-lab/weatherfiles/')
    argument_parser.add_argument('-e', nargs='*', type=int, help='Enter year to print the results for that year.',
                                 default=[])
    argument_parser.add_argument('-a', nargs='*', type=str, help='Enter year/month in this format.', default=[])
    argument_parser.add_argument('-c', nargs='*', type=str, help='Enter year/month in this format.', default=[])
    return argument_parser.parse_args()


def append_year_month(argument_list, year_month):
    """This function is appending date in argument list"""

    if valid_date(year_month[0], year_month[1]):
        if year_month[0] not in argument_list:
            year_month[1] = calendar.month_abbr[int(year_month[1])]
            argument_list.append('_'.join(year_month))
    else:
        print('date is not valid!')


def get_distinct_arguments_in_list(args):
    """This function returns distinct arguments list"""

    argument_list = []

    for arg_e in args.e:
        if valid_date(arg_e):
            argument_list.append(str(arg_e))
        else:
            print("Invalid Input for arg -e !", arg_e)

    for arg_a in args.a:
        append_year_month(argument_list, arg_a.split('/'))

    for arg_c in args.c:
        append_year_month(argument_list, arg_c.split('/'))

    return argument_list


def get_argument_flag_dict(args):
    """This function returns dictionary with flags arguments"""

    argument_dict = {}

    for arg_e in args.e:
        if 'e' not in argument_dict:
            argument_dict['e'] = []

        argument_dict['e'].append(str(arg_e))

    for arg_a in args.a:
        if 'a' not in argument_dict:
            argument_dict['a'] = []

        year_month = arg_a.split('/')
        year_month[1] = calendar.month_abbr[int(year_month[1])]
        argument_dict['a'].append('_'.join(year_month))

    for arg_c in args.c:
        if 'c' not in argument_dict:
            argument_dict['c'] = []

        year_month = arg_c.split('/')
        year_month[1] = calendar.month_abbr[int(year_month[1])]
        argument_dict['c'].append('_'.join(year_month))

    return argument_dict


if __name__ == "__main__":
    """This is the main."""

    args = parsing_arguments()
    argument_list = get_distinct_arguments_in_list(args)

    parsing_files = ParsingFiles(args.file_path, argument_list)
    all_weather_readings = parsing_files.reading_files()
    file_names = [file_name.replace('.txt', '') for file_name in parsing_files.all_files_names]

    calculations_class = CalculatingResults(all_weather_readings, argument_list, file_names)
    calculations_class.calculations()
    results = calculations_class.results

    report_printer = ReportPrinting(results, get_argument_flag_dict(args))
    report_printer.printing()

