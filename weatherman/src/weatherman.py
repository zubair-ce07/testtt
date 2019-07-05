import os
import re
import glob
import argparse
import calendar

import calc
import reportgen as rg

from ds import YearReading, MonthReading, YearResults, MonthResults, ChartResults

def valid_month(argument):
    if not re.match("\\d{4}/\d", argument):
        raise argparse.ArgumentTypeError(f"Invalid format: {argument}")
    split_date = argument.split('/')
    if int(split_date[1]) < 1 or int(split_date[1]) > 12:
        raise argparse.ArgumentTypeError(f"Invalid month value: {split_date[1]}")
    return tuple((split_date[0], split_date[1]))

def valid_year(argument):
    if re.match("\\d{4}$", argument):
        return int(argument)
    else:
        raise argparse.ArgumentTypeError(f"Invalid format: {argument}")

def valid_dir(argument):
    if os.path.exists(argument):
        return argument
    else:
        raise argparse.ArgumentTypeError(f"Invalid Path: {argument}")

parser = argparse.ArgumentParser("Display weather reports")
parser.add_argument('dir', type = valid_dir, help = "Path to Files directory")
parser.add_argument('-e', nargs = '+', action = 'store', dest = 'year', 
                    type = valid_year, help = "YYYY")
parser.add_argument('-a', nargs = '+', action = 'store', dest = 'year_month', 
                    type = valid_month, help = "YYYY/MM")
parser.add_argument('-c', nargs = '+', action = 'store', dest = 'chart', 
                    type = valid_month, help = "YYYY/MM")
parser.add_argument('-b', nargs = '+', action = 'store', dest = 'bonus', 
                    type = valid_month, help = "YYYY/MM")
args = parser.parse_args()

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
        month_name = calendar.month_abbr[int(year_month[1])]
        file_path = f"{args.dir}/Murree_weather_{year_month[0]}_{month_name}.txt"
        if os.path.exists(file_path):
            rg.month_report(calc.monthly_calc(MonthReading(file_path, year_month[0])))
        else:
            print(f"Data for {month_name} {year_month[0]} does not exist")
if args.chart:
    for chart in args.chart:
        print()
        month_name = calendar.month_abbr[int(chart[1])]
        file_path = f"{args.dir}/Murree_weather_{chart[0]}_{month_name}.txt"
        if os.path.exists(file_path):
            rg.chart_report(calc.bar_chart(MonthReading(file_path, chart[0])))
        else:
            print(f"Data for {month_name} {chart[0]} does not exist")
if args.bonus:
    for bonus in args.bonus:
        print()
        month_name = calendar.month_abbr[int(bonus[1])]
        file_path = f"{args.dir}/Murree_weather_{bonus[0]}_{month_name}.txt"
        if os.path.exists(file_path):
            rg.chart_bonus_report(calc.bar_chart(MonthReading(file_path, bonus[0])))
        else:
            print(f"Data for {month_name} {bonus[0]} does not exist")
