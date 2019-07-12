"""Weather insights"""
import sys
import math
import argparse
from parser import Parser
from calculations import weather_calculator
from reporter import Reporter


def main():

    # Command Line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path")
    parser.add_argument('-e', action='store', dest='year_to_report')
    parser.add_argument('-a', action='store', dest='month_to_report')
    parser.add_argument('-c', action='store', dest='month_to_plot')
    args = parser.parse_args()

    # Read data by using the parser.
    data, years, months = Parser().read_files(args.data_path)

    # Do calculations using the data.
    years_monthly_records = weather_calculator(
        years, months
        ).weather_calculations(data)
    per_year_records = weather_calculator(
        years, months
        ).calculate_yearly(
        years_monthly_records
        )

    # Report as the user commanded.
    if args.year_to_report:
        Reporter().yearly_report(per_year_records, args.year_to_report)
    if args.month_to_report:
        Reporter().monthly_report(years_monthly_records, args.month_to_report)
    if args.month_to_plot:
        Reporter().monthly_bar_chart(years_monthly_records, args.month_to_plot)
        Reporter().horizontal_barchart(
            years_monthly_records, args.month_to_plot
            )
    return


main()
