import argparse
from weather_data import FileReader
from reporter import *


def check_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', nargs='*')
    parser.add_argument('-a', nargs='*')
    parser.add_argument('-c', nargs='*')
    parser.add_argument('-b', nargs='*')
    parser.add_argument('file_path')
    args = parser.parse_args()
    if args.e:
        for year in args.e:
            get_max_min(FileReader(args.file_path, year))
    if args.a:
        for year_month in args.a:
            month_average(FileReader(args.file_path, year_month.split('/')[0], year_month.split('/')[1]))
    if args.c:
        for year_month in args.c:
            print_chart(FileReader(args.file_path, year_month.split('/')[0], year_month.split('/')[1]))
    if args.b:
        for year_month in args.b:
            bonus_task(FileReader(args.file_path, year_month.split('/')[0], year_month.split('/')[1]))


def main():
    check_args()


if __name__ == '__main__':
    main()