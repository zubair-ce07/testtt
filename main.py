import argparse
import datetime
import os
import sys

from avg_monthly_temperature import AvgMonthlyTemperature
from constants import Constants
from horizontal_bar_chart import HorizontalBarChart
from temperature_observer import TemperatureObserver

"""
Main class. As entry class
"""
class Main:
    @staticmethod
    def main():
        if args.year is not None:
            Main.show_annual_report(args.year, args.path)

        if args.average is not None:
            Main.show_monthly_report(args.average, args.path)

        if args.chart is not None:
            Main.show_bar_chart(args.chart, args.path)

        if args.year is None and args.average is None and args.chart is None:
            print("At least one argument is required.")
            sys.exit()

    @staticmethod
    def show_monthly_report(year_month, path):
        try:
            year_month = datetime.datetime.strptime(year_month, "%Y/%m")
            avg_monthly_temp = AvgMonthlyTemperature()
            monthly_report = avg_monthly_temp.show_monthly_report(
                year_month.strftime("%Y"),
                year_month.strftime("%b"),
                path)
            if monthly_report is None:
                print("No result found")
            else:
                value_to_print = "Highest Average: %sC\nLowest Average: %sC\n" \
                                 "Average Mean Humidity: %s%%" % (
                                     monthly_report.get(Constants.HIGHEST),
                                     monthly_report.get(Constants.LOWEST),
                                     monthly_report.get(Constants.MEAN_HUMIDITY))
                print(value_to_print)
        except ValueError as e:
            print("Enter value is wrong", e)

    @staticmethod
    def show_annual_report(year, directory):
        if year is not None and year.isdigit():
            temp_observer = TemperatureObserver()
            annual_report = temp_observer.show_annual_report(year, directory)
            if annual_report is not None:
                highest = annual_report.get(Constants.HIGHEST)
                lowest = annual_report.get(Constants.LOWEST)
                humidity = annual_report.get(Constants.HUMIDITY)
                date = highest.get(Constants.DATE)
                day = datetime.datetime.strptime(date, '%Y-%m-%d').strftime(
                    '%B %d')
                print("Highest: %sC on %s" % (highest.get(Constants.VALUE), day))
                date = lowest.get(Constants.DATE)
                day = datetime.datetime.strptime(date, '%Y-%m-%d').strftime(
                    '%B %d')
                print("Lowest: %sC on %s" % (lowest.get(Constants.VALUE), day))
                date = humidity.get(Constants.DATE)
                day = datetime.datetime.strptime(date, '%Y-%m-%d').strftime(
                    '%B %d')
                print("Humidity: %s%% on %s" % (humidity.get(
                    Constants.VALUE), day))
            else:
                print("No Result found")
        else:
            print("Entered YEAR value is wrong")

    @staticmethod
    def show_bar_chart(year_month, path):
        try:
            year_month = datetime.datetime.strptime(year_month, "%Y/%m")
            hbc = HorizontalBarChart()
            print(year_month.strftime("%B %Y"))
            hbc.show_min_max_multi_bar_chart(
                year_month.strftime("%Y"),
                year_month.strftime("%b"),
                path
            )
            print(year_month.strftime("%B %Y"))
            hbc.show_min_max_single_bar_chart(
                year_month.strftime("%Y"),
                year_month.strftime("%b"),
                path
            )
        except ValueError as e:
            print("Enter value is wrong", e)


class FullPaths(argparse.Action):
    """
    paths
    Taken from : https://gist.github.com/brantfaircloth/1443543
    """

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))


def is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


parser = argparse.ArgumentParser(description='Weather report arguments by '
                                             'm.imran')
parser.add_argument(
    '-e',
    '--year',
    help='Input should be a year e. 2015',
    required=False)
parser.add_argument(
    '-a',
    '--average',
    help='Input should be year/month e.g 2015/3',
    required=False)
parser.add_argument(
    '-c',
    '--chart',
    help='Input should be year/month e.g 2015/3',
    required=False)

parser.add_argument('path', help="The folder of files",
                    action=FullPaths, type=is_dir)

args = parser.parse_args()
Main.main()
