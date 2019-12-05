import argparse
import datetime
from constants import Reports
from report_generator import ReportGenerator
from weather_data_parser import WeatherDataParser
from weather_data_analyzer import WeatherDataAnalyzer


def main():

    args = initialize_arguments()

    parser = WeatherDataParser(args.dir_path)

    if args.e:
        show_extreme_stats(parser, int(args.e))

    if args.a:
        year_month = datetime.datetime.strptime(args.a, '%Y/%m')
        show_mean_stats(parser, year_month.month, year_month.year)

    if args.c:
        year_month = datetime.datetime.strptime(args.c, '%Y/%m')
        show_graphs(parser, year_month.month, year_month.year)


def show_extreme_stats(parser, year):
    data = parser.fetch_records_of_year(year)

    analyzer = WeatherDataAnalyzer(data)
    results = analyzer.calculate_extremes()
    if results:
        report_generator = ReportGenerator(results)
        report_generator.generate(Reports.SHOW_EXTREMES)


def show_mean_stats(parser, month, year):
    data = parser.fetch_records_of_month(month, year)
    results = WeatherDataAnalyzer(data).calculate_averages()

    if results:
        report_generator = ReportGenerator(results)
        report_generator.generate(Reports.SHOW_MEANS)


def show_graphs(parser, month, year):
    data = parser.fetch_records_of_month(month, year)
    report_generator = ReportGenerator(data)
    report_generator.generate(Reports.SHOW_GRAPHS)


def initialize_arguments():
    description = 'This is weather reports generation tool, which generates different types of reports depending ' \
                  'upon arguments.'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('dir_path', help="Path to the directory of data files")

    parser.add_argument('-e', help="For a given month, it displays the average highest temperature, average lowest "
                                   "temperature, average mean humidity")
    parser.add_argument('-a', help="For a given month, it displays the average highest temperature, average lowest"
                                   "temperature, average mean humidity.")

    parser.add_argument('-c', help="For a given month, it draws two horizontal bar charts on the console for the"
                                   "highest and lowest temperature on each day. Highest in red and lowest in blue.")

    return parser.parse_args()


if __name__ == '__main__':
    main()
