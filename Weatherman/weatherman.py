import argparse
import re
from functions import get_yearly_record
from functions import get_monthly_average
from functions import get_monthly_record_bars
from functions import get_monthly_single_line_bars

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
parser.add_argument('-e', type=str)
parser.add_argument('-a', type=str)
parser.add_argument('-c', type=str)
parser.add_argument('-d', type=str)
args = parser.parse_args()


def validate_args(value):

    regex = "^\d{4}$"
    regex_1 = "^\d{4}\/\d\d?$"
    if re.match(regex, str(value)) or re.match(regex_1, str(value)):
        return True
    else:
        print "InValid Value for {}".format(value)
        print "Please Enter 4 digit Year Value For e and Year/month number for a ,c or d"
        return


def main():

    if args.e and validate_args(args.e):
        get_yearly_record(args.filename,args.e)

    if args.a and validate_args(args.a):
        get_monthly_average(args.filename,args.a)

    if args.c and validate_args(args.c):
        get_monthly_record_bars(args.filename,args.c)

    if args.d and validate_args(args.d):
        get_monthly_single_line_bars(args.filename,args.d)


if __name__ == '__main__':
    main()

