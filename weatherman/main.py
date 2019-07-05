import argparse
from datetime import datetime

from reportgenerator import ReportCalculator, ReportPrinter
from weatherparser import WeatherParser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)

    parser.add_argument('-high_low_report', '-e', nargs='*',
                        type=lambda s: datetime.strptime(s, '%Y'))

    parser.add_argument('-avg_report', '-a', nargs='*',
                        type=lambda s: datetime.strptime(s, '%Y/%m'))

    parser.add_argument('-dual_graph_report', '-c', nargs='*',
                        type=lambda s: datetime.strptime(s, '%Y/%m'))

    parser.add_argument('-single_graph_report', '-b', nargs='*',
                        type=lambda s: datetime.strptime(s, '%Y/%m'))

    args = parser.parse_args()

    dataset_path = args.path
    weather_parser = WeatherParser(dataset_path)
    report_calculator = ReportCalculator(weather_parser)
    report_printer = ReportPrinter()

    if args.high_low_report:
        for arg in args.high_low_report:
            result = report_calculator.high_low_temperature(
                weather_parser.filtered_records(year=arg.year))
            report_printer.high_low_temperature_printer(result)

    if args.avg_report:
        for arg in args.avg_report:
            result = report_calculator.avg_temperature(
                weather_parser.filtered_records(year=arg.year,month=arg.month))
            report_printer.avg_temperature_printer(result)

    if args.dual_graph_report:
        for arg in args.dual_graph_report:
            report_printer.dual_graph_printer(
                weather_parser.filtered_records(year=arg.year, month=arg.month))

    if args.single_graph_report:
        for arg in args.single_graph_report:
            report_printer.single_graph_printer(
                weather_parser.filtered_records(year=arg.year, month=arg.month))


if __name__ == '__main__':
    main()
