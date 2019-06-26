import os
import re
import glob
import argparse
import calendar

import calc
import reportgen as rg

from ds import YearReading, MonthReading, YearResults, MonthResults, ChartResults

def valid_month(argument):
    if re.match("\\d{4}/\d", argument):
        return argument
    else:
        raise argparse.ArgumentTypeError(f"Invalid format: {argument}")

parser = argparse.ArgumentParser("Display weather reports")
parser.add_argument('dir', type = str, help = "Path to Files directory")
parser.add_argument('-e', nargs = '*', action = 'store', dest = 'year', 
                    type = int, help = "YYYY")
parser.add_argument('-a', nargs = '*', action = 'store', dest = 'year_month', 
                    type = valid_month, help = "YYYY/MM")
parser.add_argument('-c', nargs = '*', action = 'store', dest = 'chart', 
                    type = valid_month, help = "YYYY/MM")
parser.add_argument('-b', nargs = '*', action = 'store', dest = 'bonus', 
                    type = valid_month, help = "YYYY/MM")
args = parser.parse_args()

if os.path.exists(args.dir):
    if args.year:
        for year in args.year:
            print()
            dir_path = f"{args.dir}/Murree_weather_{year}_*.txt"
            filenames = glob.glob(dir_path)
            if filenames:
                rg.year_report(calc.yearly_calc(YearReading(filenames, year)))
            else:
                print(f"Data does not exist for the year {year}")
    if args.year_month:
        for year_month in args.year_month:
            print()
            split_date = year_month.split('/')
            month_num = int(split_date[1])
            if not month_num < 1 and not month_num > 12:
                month_name = calendar.month_abbr[month_num]
                file_path = f"{args.dir}/Murree_weather_{split_date[0]}_{month_name}.txt"
                if os.path.exists(file_path):
                    rg.month_report(calc.monthly_calc(MonthReading(file_path, split_date[0])))
                else:
                    print(f"Data for {month_name} {split_date[0]} does not exist")
            else:
                print(f"Invalid value of month: {month_num}")
    if args.chart:
        for chart in args.chart:
            print()
            split_date = chart.split('/')
            month_num = int(split_date[1])
            if not month_num < 1 and not month_num > 12:
                month_name = calendar.month_abbr[month_num]
                file_path = f"{args.dir}/Murree_weather_{split_date[0]}_{month_name}.txt"
                if os.path.exists(file_path):
                    rg.chart_report(calc.bar_chart(MonthReading(file_path, split_date[0])))
                else:
                    print(f"Data for {month_name} {split_date[0]} does not exist")
            else:
                print(f"Invalid value of month: {month_num}")
    if args.bonus:
        for bonus in args.bonus:
            print()
            split_date = bonus.split('/')
            month_num = int(split_date[1])
            if not month_num < 1 and not month_num > 12:
                month_name = calendar.month_abbr[month_num]
                file_path = f"{args.dir}/Murree_weather_{split_date[0]}_{month_name}.txt"
                if os.path.exists(file_path):
                    rg.chart_bonus_report(calc.bar_chart(MonthReading(file_path, split_date[0])))
                else:
                    print(f"Data for {month_name} {split_date[0]} does not exist")
            else:
                print(f"Invalid value of month: {month_num}")
            
else:
    print("Invalid path")
