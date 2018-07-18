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

    year_month = date.split('/')
    year_month[1] = calendar.month_abbr[int(year_month[1])]
    date = '_'.join(year_month)
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


def get_argument(args):
    """This function returns distinct arguments list and all arguments dictionary"""

    argument_dictionary = {}
    if args.e:
        argument_dictionary['e'] = args.e[:]

    if args.a:
        argument_dictionary['a'] = args.a[:]

    if args.c:
        argument_dictionary['c'] = args.c[:]

    return argument_dictionary


if __name__ == "__main__":
    """This is the main."""

    args = parsing_arguments()
    argument_dictionary = get_argument(args)
    parsing_files = ParsingFiles(args.file_path)
    all_weather_readings = parsing_files.reading_files()

    calculations_class = CalculatingResults(all_weather_readings)

    for key_arg in argument_dictionary.keys():
        for argument in argument_dictionary[key_arg]:
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
