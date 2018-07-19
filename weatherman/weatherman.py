import argparse
import calendar
import datetime

from calculation_class import CalculatingResults
from parsing_class import ParsingFiles
from report_class import ReportPrinting


def valid_year(year):
    """This function is checking validation of year"""
    if valid_date(year, '%Y'):
        return year


def valid_year_month(date):
    """This function is validating year/month format"""
    if valid_date(date, '%Y/%m'):
        year_month = date.split('/')
        year_month[1] = calendar.month_abbr[int(year_month[1])]
        date = '_'.join(year_month)
    return date


def valid_date(date, date_format):
    """This function is checking validation of date"""
    try:
        datetime.datetime.strptime(date, date_format)
    except ValueError:
        raise
    return True


def parsing_arguments():
    """This function is parsing argument"""

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('file_path', type=str, help='Path to the weatherdata files directory.',
                                 default='/home/muhammad/training-tasks/the-lab/weatherfiles/')
    argument_parser.add_argument('-e', nargs='*', type=valid_year, help='Enter year to print the results for that year',
                                 default=['2005'])
    argument_parser.add_argument('-a', nargs='*', type=valid_year_month, help='Enter year/month to print average of '
                                                                              'maximum temperature, minimum temperature'
                                                                              ' and mean humidity.', default=[])
    argument_parser.add_argument('-c', nargs='*', type=valid_year_month, help='Enter year/month to plot a bar chart of '
                                                                              'maximum temperature and minimum '
                                                                              'temperature on each day of given month',
                                 default=[])
    return argument_parser.parse_args()


if __name__ == "__main__":
    """This is the main."""

    args = parsing_arguments()
    parsing_files = ParsingFiles(args.file_path)
    all_weather_readings = parsing_files.reading_files()

    calculations_class = CalculatingResults(all_weather_readings)

    for argument in args.e:
        calculations_class.calculate_results_for_year(argument)
        report_class = ReportPrinting(calculations_class.results)
        report_class.print_results_for_year(argument)

    for argument in args.a:
        calculations_class.calculate_average_results_for_month(argument)
        report_class = ReportPrinting(calculations_class.results)
        report_class.print_results_for_month(argument)

    for argument in args.c:
        calculations_class.calculate_month_chart(argument)
        report_class = ReportPrinting(calculations_class.results)
        report_class.plot_chart_for_month(argument)
