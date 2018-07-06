#!/usr/bin/python
import sys
import getopt
import glob
from DataStructure import Year, Month
from Parser import parse_month as psm
from Computer import *
from Reporter import *

data = {}


def load_files(path):
    for file in glob.glob(path+'Murree_weather_*_*.txt'):
        y_m = str.split(file, '_')
        y = y_m[2]
        m = y_m[3][:3]

        data_rows = open(file, 'r').readlines()[1:]
        month = Month(data_rows)

        if y in data:
            data[y][m] = month
        else:
            data[y] = Year()
            data[y][m] = month


def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "a:c:e:")
        load_files(argv[0])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-e':
            report_e(result_e(arg, data))
        elif opt == "-c":
            month, year = psm(arg)
            report_c(result_c(month, year, data))
        elif opt == "-a":
            month, year = psm(arg)
            report_a(result_a(month, year, data))


if __name__ == "__main__":
    main(sys.argv[1:])
