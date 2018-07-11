#!/usr/bin/python

from weatheregister import WeatherRegister
import argparse
from parser import parse_month as psm
from reporter import Reporter


def main(argv):
    records = WeatherRegister()
    if not argv.e and argv.a and argv.c:
        parser.error('No action requested, add at-least one action (-e, -a, -c)')
    records.read_dir(argv.path)
    reporter = Reporter(records)
    if argv.e:
        reporter.report_e(argv.e)
    if argv.a:
        month, year = psm(argv.a)
        reporter.report_a(month, year)
    if argv.c:
        month, year = psm(argv.c)
        reporter.report_c(month, year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-e')
    parser.add_argument('-a')
    parser.add_argument('-c')
    args = parser.parse_args()
    main(args)
