import argparse
from datetime import datetime

from reportgenerator import ReportGenerator
from weatherparser import WeatherParser


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('path')

    # the first argument will be used as the property name and
    # rest of the positional arguments can be used in terminals
    # as flags
    parser.add_argument('-high_low_report', '-e', nargs=1, action='append')
    parser.add_argument('-avg_report', '-a', nargs=1, action='append')
    parser.add_argument('-dual_graph_report', '-c', nargs=1, action='append')
    parser.add_argument('-single_graph_report', '-b', nargs=1, action='append')
    args = parser.parse_args()

    dataset_path = args.path
    weather_parser = WeatherParser(dataset_path)
    report_generator = ReportGenerator(weather_parser)

    monthly_date_format = '%Y/%m'

    if args.high_low_report:
        for arg in args.high_low_report:
            input_date = datetime.strptime(arg[0], '%Y').date()
            report_generator.high_low_temperature(year=input_date.year)

    if args.avg_report:
        for arg in args.avg_report:
            input_date = datetime.strptime(arg[0], monthly_date_format).date()
            report_generator.avg_temperature(year=input_date.year,
                                             month=input_date.month)

    if args.dual_graph_report:
        for arg in args.dual_graph_report:
            input_date = datetime.strptime(arg[0], monthly_date_format).date()
            report_generator.high_low_temperature_dual_graph(year=input_date.year,
                                                             month=input_date.month)

    if args.single_graph_report:
        for arg in args.single_graph_report:
            input_date = datetime.strptime(arg[0], monthly_date_format).date()
            report_generator.high_low_temperature_single_graph(year=input_date.year,
                                                               month=input_date.month)


if __name__ == '__main__':
    main()
