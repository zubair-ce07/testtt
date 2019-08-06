import os
import calendar
import argparse
import csv
import argparse
from year_report import *
from month_report import *
from chart_report import *


def generate_file_namaes(args, file_names):

    if args.e:

        for month_idx in range(1, 13):
            temp = (f"Murree_weather_{args.e}_{calendar.month_name[month_idx][:3]}.txt")
            try:
                with open(temp, "r") as csvFile:
                    reader = csv.reader(csvFile)
                csvFile.close()
                file_names.append(temp)
            except IOError:
                print(f"{temp} file not found...")
    elif args.a:
        year, month_index = args.a.split('/')
        file_names.append(f"Murree_weather_{year}_{calendar.month_name[int(month_index)][:3]}.txt")
    elif args.c:
        year, month_index = args.c.split('/')
        file_names.append(f"Murree_weather_{year}_{calendar.month_name[int(month_index)][:3]}.txt")
    elif args.d:
        year, month_index = args.d.split('/')
        file_names.append(f"Murree_weather_{year}_{calendar.month_name[int(month_index)][:3]}.txt")


def main():

    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('-e', help='year report')
    parser.add_argument('-a', help='month report')
    parser.add_argument('-c', help='chart report')
    parser.add_argument('-d', help='chart report bonus')
    args = parser.parse_args()

    file_names = []

    for opt, value in args.__dict__.items():
        file_names.clear()

        if opt == 'e' and value is not None:
            generate_file_namaes(args, file_names)
            obj = YearReport()
            obj.generate_year_report(file_names)
        elif opt == 'a' and value is not None:
            obj = MonthReport()
            generate_file_namaes(args, file_names)
            obj.generate_month_report(file_names)
        elif opt == 'c' and value is not None:
            obj = ChartReport()
            generate_file_namaes(args, file_names)
            obj.generate_chart_report(file_names,0)
        elif opt == 'd' and value is not None:
            generate_file_namaes(args, file_names)
            obj = ChartReport()
            obj.generate_chart_report(file_names,1)


if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')
    main()

