"""
Module is able to take input from command-line and generate 4 types
of reports of the weatherman dataset. This module is tightly bound
to the aforementioned dataset only.
"""

import argparse

from weatherparser import YearlyWeatherParser, MonthlyWeatherParser
from reportgenerator import HighLowReportGenerator, \
                            AverageTemperatureReportGenerator, \
                            HighLowTemperatureGraphReportGenerator, \
                            HighLowTemperatureSingleGraphReportGenerator


def main():

    # handling command-line arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='relative path to the dataset')
    parser.add_argument('-e', nargs=1, required=False, action='append')
    parser.add_argument('-a', nargs=1, required=False, action='append')
    parser.add_argument('-c', nargs=1, required=False, action='append')
    parser.add_argument('-b', nargs=1, required=False, action='append')
    args = parser.parse_args()  # parsed arguments
    dataset_path = args.path

    # argparse holds a separate list for each argument flag/name type
    # e.g -e will have arguments like ['2009', '2008']
    #
    # So a for loop for each flag arguments works best here
    # also it does not return an empty list but it return a None
    if args.e is not None:
        for arg in args.e:

            # parsing data
            yearly_parser = YearlyWeatherParser(path=dataset_path,
                                                year=int(arg[0]))
            weather_data = yearly_parser.parse()

            # all types of ReportGenerator(s) take weather_data
            # and generate report
            report_generator = HighLowReportGenerator()
            report_generator.generate(weather_data)

    if args.a is not None:
        for arg in args.a:
            year, month = arg[0].split('/')  # arg format is ['2006/3']
            monthly_parser = MonthlyWeatherParser(path=dataset_path,
                                                  month=int(month),
                                                  year=int(year))
            weather_data = monthly_parser.parse()
            report_generator = AverageTemperatureReportGenerator()
            report_generator.generate(weather_data)

    if args.c is not None:
        for arg in args.c:
            year, month = arg[0].split('/')  # arg format is ['2006/3']
            monthly_parser = MonthlyWeatherParser(path=dataset_path,
                                                  month=int(month),
                                                  year=int(year))
            weather_data = monthly_parser.parse()
            report_generator = HighLowTemperatureGraphReportGenerator()
            report_generator.generate(weather_data)

    if args.b is not None:
        for arg in args.b:
            year, month = arg[0].split('/')  # arg format is ['2006/3']
            monthly_parser = MonthlyWeatherParser(path=dataset_path,
                                                  month=int(month),
                                                  year=int(year))
            weather_data = monthly_parser.parse()
            report_generator = HighLowTemperatureSingleGraphReportGenerator()
            report_generator.generate(weather_data)


if __name__ == '__main__':
    main()
