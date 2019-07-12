import argparse
from weather_data import FileReader
from reporter import *


def check_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', nargs='*',
                        help='Full Year Report')
    parser.add_argument('-a', nargs='*',
                        help='Average of one month')
    parser.add_argument('-c', nargs='*',
                        help='Generate Chart of one month')
    parser.add_argument('file_path',
                        help='Directory to data, use relative path like dir/to/files')
    args = parser.parse_args()
    if args.e:
        for year in args.e:
            get_extreme_weather(FileReader(args.file_path, year))
    if args.a:
        for year_month in args.a:
            get_month_average(FileReader(args.file_path, year_month.split(
                '/')[0], year_month.split('/')[1]))
    if args.c:
        for year_month in args.c:
            print_weather_graph(
                FileReader(args.file_path, year_month.split(
                    '/')[0], year_month.split('/')[1]))

def main():
    check_args()


if __name__ == '__main__':
    main()