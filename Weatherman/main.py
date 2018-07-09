import argparse
from processor_file import Driver


def validate_argument(argument):
    try:
        year, month = argument.split('/')
    except:
        raise ValueError()
    if not int(year) or not int(month) in range(1, 13):
        raise ValueError()
    return argument

def main():
    parser = argparse.ArgumentParser(description='Report will be generated according to the Arguments')
    parser.add_argument('directory', help='Enter the directory')
    parser.add_argument('-e', '--type_e', type=int, help='Annual Report')
    parser.add_argument('-a', '--type_a', type=validate_argument, help='Monthly Report year/month')
    parser.add_argument('-c', '--type_c', type=validate_argument, help='Dual Bar Chart year/month')
    parser.add_argument('-d', '--type_d', type=validate_argument, help='Single Bar Chart year/month')
    args = parser.parse_args()
    Driver(args)


if __name__ == '__main__':
    main()
