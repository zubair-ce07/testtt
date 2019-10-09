import argparse
import glob
import sys
import csv

from weather_report import WeatherReport

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='month_avg_stats')
    parser.add_argument('-c', dest='month_min_max_bar_stats')
    parser.add_argument('-e', dest='year_min_max_stats')
    parser.add_argument('path_to_files')

    args = parser.parse_args()

    if(not(args.month_avg_stats or args.month_min_max_bar_stats or args.year_min_max_stats)):
        print("Specify a flag and date")
        return

    if(args.month_avg_stats):
        report = WeatherReport(args.month_avg_stats, args.path_to_files)
        report.calc_month_avg_stats()
    elif(args.month_min_max_bar_stats):
        report = WeatherReport(args.month_min_max_bar_stats, args.path_to_files)
        report.calc_month_min_max_stats()
    elif(args.year_min_max_stats):
        report = WeatherReport(args.year_min_max_stats, args.path_to_files)
        report.calculate_year_stats()


if __name__ == '__main__':
    main(sys.argv[1:])
