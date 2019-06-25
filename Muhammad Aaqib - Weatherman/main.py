import weather
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the files directory")
    parser.add_argument("date", help="""Year/Month to find weather's
                         calculations""")
    parser.add_argument("-e", "--year", help="""Displays annual statistics of
                         weather""", action="store_true")
    parser.add_argument("-a", "--month", help="""Displays month's statistics
                        of weather""", action="store_true")
    parser.add_argument("-c", "--chart", help="""Plots bar chart against the month's
                        statistics of weather""", action="store_true")
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    directory_path = args.path
    date = args.date
    parser = weather.FileParser()
    weather_record = parser.parse_file(directory_path)

    if weather_record:
        if args.year:
            annual_stats = weather.WeatherAnalysis.get_annual_stats(
                           weather_record, date)
            weather.ResultPrinter.print_annual_report(annual_stats)

        if args.month:
            month_stats = weather.WeatherAnalysis.get_month_stats(
                          weather_record, date)
            weather.ResultPrinter.print_monthly_report(month_stats)

        if args.chart:
            chart_data = weather.WeatherAnalysis.get_chart_data(
                         weather_record, date)
            weather.ResultPrinter.plot_month_barchart(chart_data)
            weather.ResultPrinter.plot_component_barchart(chart_data)


if __name__ == '__main__':
    main()
