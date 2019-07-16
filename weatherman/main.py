"""Weather insights"""
import argparse
from parser import Parser
from calculations import WeatherCalculator
from reporter import Reporter


def main():

    # Command Line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path")
    parser.add_argument('-e', action='store', dest='year_to_report')
    parser.add_argument('-a', action='store', dest='month_to_report')
    parser.add_argument('-c', action='store', dest='month_to_plot')
    args = parser.parse_args()

    # Report as the user commanded.
    if args.year_to_report:
        data = Parser().read_files(args.data_path, year=args.year_to_report)
        yearly_calculations = WeatherCalculator().calculate_weather(data)
        print('\n')
        Reporter().yearly_report(yearly_calculations)
        print('\n')

    if args.month_to_report:
        # Read data by using the parser.
        data = Parser().read_files(args.data_path, month=args.month_to_report)
        monthly_calculations = WeatherCalculator().calculate_weather(data)
        print('\n')
        Reporter().monthly_report(monthly_calculations)
        print('\n')

    if args.month_to_plot:
        data = Parser().read_files(args.data_path, month=args.month_to_plot)
        print('\n')
        Reporter().monthly_bar_chart(data)
        print('\n')
        Reporter().horizontal_barchart(data)
        print('\n')


if __name__ == "__main__":
    main()
