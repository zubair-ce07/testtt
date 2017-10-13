import sys,argparse

from functions import year,month

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
parser.add_argument('-e', type=str)
parser.add_argument('-a', type=str)
args = parser.parse_args()


def main():

    if args.e:
        year(args)

    elif args.a:
        month(args)

    else:
        print 'invalid'    # just for time being will add more functionality


main()
