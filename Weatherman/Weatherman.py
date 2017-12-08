import argparse
import re
import datetime

from functions import read_files_for_arguments


def validate_args(value):

    regex_1 = "^\d{4}.\d\d?$"

    if re.match(regex_1 , value):
        return value
    else:
        print 'InValid Arguments Value For {0}'.format(value)
        print 'For Arguments a , c and d Enter Value Like this 2005/07 \n'


def validate_args_e(value):

    regex = "^\d{4}$"
    if re.match(regex , value):
        return value
    else:
        print 'InValid Arguments Value For {0}'.format(value)
        print 'Enter a value of year in 4 Digits for argument e\n'


def argument_values(argument):

    if len(argument) == 4:
        date = datetime.datetime.strptime(argument, '%Y')
        arg_values = {'year': date.strftime("%Y")}
    else:
        date = datetime.datetime.strptime(argument, "%Y/%m")
        arg_values = {'year' : date.strftime("%Y"), 'month': date.strftime("%b")}

    return arg_values

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
parser.add_argument('-e', type=validate_args_e)
parser.add_argument('-a', type=validate_args)
parser.add_argument('-c', type=validate_args)
parser.add_argument('-d', type=validate_args)
args = parser.parse_args()


def main():

    if args.e:
        args.e = argument_values(args.e)

    if args.a:
        args.a = argument_values(args.a)

    if args.c:
        args.c = argument_values(args.c)

    if args.d:
        args.d = argument_values(args.d)

    read_files_for_arguments(args.filename, args.e, args.a , args.c ,args.d)




if __name__ == '__main__':
    main()

