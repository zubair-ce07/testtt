#!/usr/bin/python
import datetime
from weather_register import WeatherRegister
import argparse
from reporter import Reporter


def parse_month(string):
    parts = str.split(string, '/')
    return datetime.date(int(parts[0]), int(parts[1]), 1).strftime("%B"), parts[0]


def main(argv):
    if not argv.e and argv.a and argv.c:
        parser.error('No action requested, add at-least one action (-e, -a, -c)')
    if argv.e:
        records = WeatherRegister()
        records.read_dir(argv.path, argv.e)
        reporter = Reporter(records)
        reporter.report_for_e()
    if argv.a:
        month, year = parse_month(argv.a)
        records = WeatherRegister()
        records.read_dir(argv.path, year, month)
        reporter = Reporter(records)
        reporter.report_for_a()
    if argv.c:
        month, year = parse_month(argv.c)
        records = WeatherRegister()
        records.read_dir(argv.path, year, month)
        reporter = Reporter(records)
        reporter.report_for_c()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-e')
    parser.add_argument('-a')
    parser.add_argument('-c')
    args = parser.parse_args()
    main(args)
