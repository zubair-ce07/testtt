import Weather
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("date", help="""Year/Month to find weather's
                         calculations""")
    parser.add_argument("-e", "--yearly", help="""Display yearly weather
                         statistics""", action="store_true")
    parser.add_argument("-a", "--monthly", help="""Display yearly weather
                         statistics""", action="store_true")
    parser.add_argument("-c", "--graphically", help="""Plot the bar chart of
                         weather stats of a month""", action="store_true")
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    date = args.date
    result_printer = Weather.ResultPrinter()
    weather_record = Weather.parse_file()

    if args.yearly:
        annual_stats = Weather.get_annual_stats(weather_record, date)
        result_printer.print_annual_report(annual_stats)

    if args.monthly:
        monthly_stats = Weather.get_monthly_stats(weather_record, date)
        result_printer.print_monthly_report(monthly_stats)

    if args.graphically:
        chart_data = Weather.get_chart_data(weather_record, date)
        result_printer.plot_month_barchart(chart_data)
        result_printer.plot_component_barchart(chart_data)


if __name__ == '__main__':
    main()
