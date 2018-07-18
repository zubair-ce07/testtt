import argparse
import calendar
import datetime

from calculation_class import CalculatingResults
from parsing_class import ParsingFiles
from report_class import ReportPrinting


def valid_year(date):
    """This function is checking validation of year"""
    try:
        datetime.datetime.strptime(date, '%Y')
    except ValueError:
        raise
    return date


def valid_date(date):
    """This function is checking validation of date"""
    try:
        datetime.datetime.strptime(date, '%Y/%m')
    except ValueError:
        raise
    return date


def parsing_arguments():
    """This function is parsing argument"""

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('file_path', type=str, help='Path to the weatherdata files directory.',
                                 default='/home/muhammad/training-tasks/the-lab/weatherfiles/')
    argument_parser.add_argument('-e', nargs='*', type=valid_year, help='Enter year to print the results for that year',
                                 default=[])
    argument_parser.add_argument('-a', nargs='*', type=valid_date, help='Enter year/month to print average of maximum '
                                                                        'temperature, minimum temperature and '
                                                                        'mean humidity.', default=[])
    argument_parser.add_argument('-c', nargs='*', type=valid_date, help='Enter year/month to plot a bar chart of '
                                                                        'maximum temperature and minimum temperature '
                                                                        'on each day of given month', default=[])
    return argument_parser.parse_args()


def append_year_month(argument_list, year_month):
    """This function is appending date in argument list"""
    year_month[1] = calendar.month_abbr[int(year_month[1])]
    if year_month[0] not in argument_list:
        argument_list.append('_'.join(year_month))


def get_argument(args):
    """This function returns distinct arguments list and all arguments dictionary"""

    argument_list = []
    argument_dict = {}

    for arg_e in args.e:
        if arg_e:
            argument_list.append(str(arg_e))
            if 'e' not in argument_dict:
                argument_dict['e'] = []
            argument_dict['e'].append(arg_e)

    for arg_a in args.a:
        if arg_a:
            year_month = arg_a.split('/')
            append_year_month(argument_list, year_month)
            if 'a' not in argument_dict:
                argument_dict['a'] = []
            argument_dict['a'].append('_'.join(year_month))

    for arg_c in args.c:
        if arg_c:
            year_month = arg_c.split('/')
            append_year_month(argument_list, year_month)
            if 'c' not in argument_dict:
                argument_dict['c'] = []
            argument_dict['c'].append('_'.join(year_month))

    return argument_list, argument_dict


if __name__ == "__main__":
    """This is the main."""

    args = parsing_arguments()
    argument_list, argument_dict = get_argument(args)

    parsing_files = ParsingFiles(args.file_path, argument_list)
    all_weather_readings = parsing_files.reading_files()

    calculations_class = CalculatingResults(all_weather_readings)

    for key_arg in argument_dict.keys():
        for argument in argument_dict[key_arg]:
            if argument:
                if key_arg == 'e':
                    calculations_class.calculate_results_for_year(argument)
                    report_class = ReportPrinting(calculations_class.results)
                    report_class.print_results_for_year(argument)

                if key_arg == 'a':
                    calculations_class.calculate_average_results_for_month(argument)
                    report_class = ReportPrinting(calculations_class.results)
                    report_class.print_results_for_month(argument)

                if key_arg == 'c':
                    calculations_class.calculate_month_chart(argument)
                    report_class = ReportPrinting(calculations_class.results)
                    report_class.plot_chart_for_month(argument)
