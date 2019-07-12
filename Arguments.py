from datetime import datetime
import argparse

def argument_parse():
    p = argparse.ArgumentParser()
    p.add_argument('file_path', help='Local File Path on Your Machine')
    p.add_argument('-e', '-yearly', type=lambda argument:
    datetime.strptime(argument, '%Y'), nargs="*")
    p.add_argument('-a', '-monthly', type=lambda argument:
    datetime.strptime(argument, '%Y/%m'), nargs="*")
    p.add_argument('-b', '-bonus', type=lambda argument:
    datetime.strptime(argument, '%Y/%m'), nargs="*")
    p.add_argument('-c', '-chart', type=lambda argument:
    datetime.strptime(argument, '%Y/%m'), nargs="*")
    return p.parse_args()