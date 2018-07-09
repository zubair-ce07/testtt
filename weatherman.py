#!/usr/bin/python

from WeatherRecord import WeatherRegister
import argparse
from Parser import parse_month as psm
from Computer import *
from Reporter import *


def main(argv):
    records = WeatherRegister()
    if not argv.e or argv.a or argv.c:
        parser.error('No action requested, add at-least one action (-e, -a, -c)')
    records.read_dir(argv.path)
    if argv.e:
        report_e(result_e(argv.e, records))
    if argv.c:
        month, year = psm(argv.c)
        report_c(result_c(month, year, records))
    if argv.a:
        month, year = psm(argv.a)
        report_c(result_c(month, year, records))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-e')
    parser.add_argument('-a')
    parser.add_argument('-c')
    args = parser.parse_args()
    main(args)
