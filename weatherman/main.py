import argparse

from weatherparser import WeatherParser
from reportgenerator import ReportGenerator


def _monthly_parser_helper(arg_str, weather_parser):
    year, month = arg_str[0].split('/')
    return weather_parser.monthly_weather_parser(month=int(month), year=int(year))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')

    # the first argument will be used as the property name and
    # rest of the positional arguments can be used in terminals
    # as flags
    parser.add_argument('-high_low_report', '-e', nargs=1, required=False, action='append')
    parser.add_argument('-avg_report', '-a', nargs=1, required=False, action='append')
    parser.add_argument('-dual_graph_report', '-c', nargs=1, required=False, action='append')
    parser.add_argument('-single_graph_report', '-b', nargs=1, required=False, action='append')
    args = parser.parse_args()
    dataset_path = args.path

    weather_parser = WeatherParser(dataset_path)
    report_generator = ReportGenerator()

    if args.high_low_report is not None:
        for arg in args.high_low_report:
            weather_records = weather_parser.yearly_weather_parser(year=int(arg[0]))
            report_generator.high_low_temperature(weather_records)

    if args.avg_report is not None:
        for arg in args.avg_report:
            weather_records = _monthly_parser_helper(arg, weather_parser)
            report_generator.avg_temperature(weather_records)

    if args.dual_graph_report is not None:
        for arg in args.dual_graph_report:
            weather_records = _monthly_parser_helper(arg, weather_parser)
            report_generator.high_low_temperature_dual_graph(weather_records)

    if args.single_graph_report is not None:
        for arg in args.single_graph_report:
            weather_records = _monthly_parser_helper(arg, weather_parser)
            report_generator.high_low_temperature_single_graph(weather_records)


if __name__ == '__main__':
    main()
