import argparse
from weatheranalyzer import WeatherReporter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Path of the data directory")
    parser.add_argument("-e", help="Processing Year", default='')
    parser.add_argument("-a", help="Processing Year/MonthNumber", default='')
    parser.add_argument("-c", help="Processing Chart Year/MonthNumber", default='')
    parser.add_argument("-b", help="Processing Sinle-line Chart Year/MonthNumber", default='')
    args = parser.parse_args()

    reporting = WeatherReporter()
    reporting.start(args)