import sys,argparse

from functions import year,month,month_bars

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
parser.add_argument('-e', type=str)
parser.add_argument('-a', type=str)
parser.add_argument('-c', type=str)
args = parser.parse_args()


def main():

    if args.e:
        year(args)

    if args.a:
        month(args)

    if args.c:
        month_bars(args)
    else:
        print 'Invalid parameters'



main()

