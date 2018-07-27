import argparse
import calendar
import datetime

from weather_statistics_calculation import WeatherStatisticsCalculation
from weather_data_parsing import WeatherDataParsing
from weather_statistics_report import WeatherStatisticsReport


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
    weather_data_parsing = WeatherDataParsing(args.file_path)
    all_weather_readings = weather_data_parsing.reading_files()
    weather_statistics_calculation = WeatherStatisticsCalculation(all_weather_readings)

    for argument in args.e:
        weather_statistics_calculation.get_extrema_statistics(argument)
        weather_statistics_report = WeatherStatisticsReport(weather_statistics_calculation.results)
        weather_statistics_report.print_extrema_statistics(argument)

    for argument in args.a:
        weather_statistics_calculation.get_average_statistics(argument)
        weather_statistics_report = WeatherStatisticsReport(weather_statistics_calculation.results)
        weather_statistics_report.print_average_statistics(argument)

    for argument in args.c:
        weather_statistics_calculation.get_bar_chart_records(argument)
        weather_statistics_report = WeatherStatisticsReport(weather_statistics_calculation.results)
        weather_statistics_report.plot_chart(argument)
