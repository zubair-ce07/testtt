import argparse

from parser import Parser
from calculations import WeatherCalculator
from reporter import Reporter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path")
    parser.add_argument('-e', action='store', dest='year_to_report')
    parser.add_argument('-a', action='store', dest='month_to_report')
    parser.add_argument('-c', action='store', dest='month_to_plot')
    args = parser.parse_args()

    if args.year_to_report:
        data = Parser(args.data_path, args.year_to_report).read_files()
        yearly_calculations = WeatherCalculator(data).calculate_weather()
        print('\n')
        Reporter().yearly_report(yearly_calculations)
        print('\n')

    if args.month_to_report:
        data = Parser(args.data_path, args.month_to_report).read_files()
        monthly_calculations = WeatherCalculator(data).calculate_weather()
        print('\n')
        Reporter().monthly_report(monthly_calculations)
        print('\n')

    if args.month_to_plot:
        data = Parser(args.data_path, args.month_to_plot).read_files()
        print('\n')
        Reporter().monthly_bar_chart(data)
        print('\n')
        Reporter().horizontal_barchart(data)
        print('\n')

if __name__ == "__main__":
    main()
