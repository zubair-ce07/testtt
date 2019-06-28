import weather
import argparse
import re


def validate_month(input_month):
    month_format = re.compile(r"\d{4}(-|/)\d{1,2}$")
    if not month_format.match(input_month):
        raise argparse.ArgumentTypeError
        
    return input_month


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the files directory")
    parser.add_argument("-e", "--year", help="Displays annual statistics of \
                         weather", action="append", type=int)
    parser.add_argument("-a", "--month", help="Displays month's statistics \
                        of weather", action="append", type=validate_month)
    parser.add_argument("-c", "--chart", help="Plots bar chart against the \
                        month's statistics of weather", action="append",
                        type=validate_month)
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
        for year in args.year or []:
            annual_stats = weather_stats.get_annual_stats(weather_record,
                                                            year)
            result_printer.print_annual_report(annual_stats)

        for month in args.month or []:
            print("Bewaja")
            month_stats = weather_stats.get_month_stats(weather_record, month)
            result_printer.print_monthly_report(month_stats, month)
    
        for month in args.chart or []:
            chart_data = weather_stats.get_chart_data(weather_record,
                                                        month)
            result_printer.plot_month_barchart(chart_data)
            result_printer.plot_month_horizontal_barchart(chart_data)


if __name__ == '__main__':
    main()
