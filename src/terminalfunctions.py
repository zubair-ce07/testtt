import re
import os

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
