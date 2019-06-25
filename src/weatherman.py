import os
import re
import argparse
import calendar

import calc
import reportgen as rg

from ds import YearReading, MonthReading, YearResults, MonthResults, ChartResults

def validate_arguments(args):
    if not os.path.exists(args.dir):
        print("Invalid path")
        return False
    if args.year_month:
        for year_month in args.year_month:
            if not re.match("\\d{4}/\\d{2}", year_month) and not re.match("\\d{4}/\\d{1}", year_month):
                print("Wrong format!")
                return False
    if args.chart:
        for chart in args.chart:
            if not re.match("\\d{4}/\\d{2}", chart) and not re.match("\\d{4}/\\d{1}", chart):
                print("Wrong format!")
                return False
    if args.bonus:
        for bonus in args.bonus:
            if not re.match("\\d{4}/\\d{2}", bonus) and not re.match("\\d{4}/\\d{1}", bonus):
                print("Wrong format!")
                return False
    return True

parser = argparse.ArgumentParser("Display weather reports")

parser.add_argument('dir', type = str, help = "Path to Files directory")
parser.add_argument('-e', nargs = '*', action = 'store', dest = 'year', type = int, help = "YYYY (for year report)")
parser.add_argument('-a', nargs = '*', action = 'store', dest = 'year_month', type = str, help = "YYYY/MM (for month report)")
parser.add_argument('-c', nargs = '*', action = 'store', dest = 'chart', type = str, help = "YYYY/MM (for bar chart)")
parser.add_argument('-b', nargs = '*', action = 'store', dest = 'bonus', type = str, help = "YYYY/MM (for bonus bar chart")

args = parser.parse_args()

if validate_arguments(args) == True:
    if args.year:
        for year in args.year:
            print()
            if not year < 2004 and not year > 2016:
                    year = YearReading(args.dir, str(year))
                    year_results = calc.yearly_calc(year)
                    rg.year_report(year_results)
            else:
                print(f"Data for the year {year} does not exist")
    if args.year_month:
        for year_month in args.year_month:
            print()
            split_date = year_month.split('/')
            month_num = int(split_date[1])
            if not month_num < 1 and not month_num > 12:
                month_name = calendar.month_abbr[month_num]
                file_path = f"{args.dir}/Murree_weather_{split_date[0]}_{month_name}.txt"
                if os.path.exists(file_path):
                    month = MonthReading(file_path, split_date[0])
                    month_results = calc.monthly_calc(month)
                    rg.month_report(month_results)
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
                    month = MonthReading(file_path, split_date[0])
                    chart_results = calc.bar_chart(month)
                    rg.chart_report(chart_results)
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
                    month = MonthReading(file_path, split_date[0])
                    bonus_results = calc.bar_chart(month)
                    rg.chart_bonus_report(bonus_results)
                else:
                    print(f"Data for {month_name} {split_date[0]} does not exist")
            else:
                print(f"Invalid value of month: {month_num}")
