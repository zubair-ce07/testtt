import weather
import argparse
import re


def month_regex_type(input_month):
    month_format = re.compile("\\d{4}(-|/)\\d{1,2}$")
    if not month_format.match(input_month):
        raise argparse.ArgumentTypeError
        
    return input_month


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the files directory")
    parser.add_argument("-e", "--year", help="""Displays annual statistics of
                         weather""", action="append", type=int)
    parser.add_argument("-a", "--month", help="""Displays month's statistics
                        of weather""", action="append", type=month_regex_type)
    parser.add_argument("-c", "--chart", help="""Plots bar chart against the
                        month's statistics of weather""", action="append",
                        type=month_regex_type)
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    directory_path = args.path
    parser = weather.FileParser()
    weather_stats = weather.WeatherAnalysis()
    result_printer = weather.ResultPrinter()
    weather_record = parser.parse_files(directory_path)
    if weather_record:
        if args.year:
            for year in args.year:
                annual_stats = weather_stats.get_annual_stats(weather_record,
                                                              year)
                result_printer.print_annual_report(annual_stats)

        if args.month:
            for month in args.month:
                month_stats = weather_stats.get_month_stats(weather_record, month)
                result_printer.print_monthly_report(month_stats, month)
        
        if args.chart:
            for month in args.chart:
                chart_data = weather_stats.get_chart_data(weather_record,
                                                            month)
                result_printer.plot_month_barchart(chart_data)
                result_printer.plot_component_barchart(chart_data)


if __name__ == '__main__':
    main()
