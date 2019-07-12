from datetime import datetime
import argparse

def argument_parse():
    p = argparse.ArgumentParser()
    p.add_argument('file_path', help='Local File Path on Your Machine')
    p.add_argument('-e', '-yearly', type=lambda arg: datetime.strptime(arg, '%Y'), nargs="*")
    p.add_argument('-a', '-monthly', type=lambda arg: datetime.strptime(arg, '%Y/%m'), nargs="*")
    p.add_argument('-b', '-bonus', type=lambda arg: datetime.strptime(arg, '%Y/%m'), nargs="*")
    p.add_argument('-c', '-chart', type=lambda arg: datetime.strptime(arg, '%Y/%m'), nargs="*")
    return p.parse_args()