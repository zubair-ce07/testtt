import argparse
from weather_readings_reader import WeatherReadingsReader


def validate_argument(argument):
    try:
        year, month = argument.split('/')
    except:
        raise argparse.ArgumentTypeError("Argument Type Error. Enter in the form of int/int")
    if not int(year) or not int(month) in range(1, 13):
        raise argparse.ArgumentTypeError("Year should be an integer month should be an integer from 1-12")
    return argument


def main():
    parser = argparse.ArgumentParser(description='Report will be generated according to the Arguments')
    parser.add_argument('directory', help='Enter the directory')
    parser.add_argument('-e', '--type_e', type=int, help='Annual Report')
    parser.add_argument('-a', '--type_a', type=validate_argument, help='Monthly Report year/month')
    parser.add_argument('-c', '--type_c', type=validate_argument, help='Dual Bar Chart year/month')
    parser.add_argument('-d', '--type_d', type=validate_argument, help='Single Bar Chart year/month')
    args = parser.parse_args()
    WeatherReadingsReader(args)


if __name__ == '__main__':
    main()
