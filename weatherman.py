#!/usr/bin/python

from weatheregister import WeatherRegister
import argparse
from parser import parse_month as psm
from reporter import Reporter


def main(argv):
    if not argv.e and argv.a and argv.c:
        parser.error('No action requested, add at-least one action (-e, -a, -c)')
    if argv.e:
        records = WeatherRegister()
        records.read_dir(argv.path, argv.e)
        reporter = Reporter(records)
        reporter.report_e()
    if argv.a:
        month, year = psm(argv.a)
        records = WeatherRegister()
        records.read_dir(argv.path, year, month)
        reporter = Reporter(records)
        reporter.report_a()
    if argv.c:
        month, year = psm(argv.c)
        records = WeatherRegister()
        records.read_dir(argv.path, year, month)
        reporter = Reporter(records)
        reporter.report_c()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-e')
    parser.add_argument('-a')
    parser.add_argument('-c')
    args = parser.parse_args()
    main(args)
