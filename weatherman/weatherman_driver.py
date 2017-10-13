import argparse
import glob
import os

from weatherman import WeatherReport


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', '--path')
    parser.add_argument('-e', default=None, required=False)
    parser.add_argument('-c', default=None, required=False)
    parser.add_argument('-a', default=None, required=False)
    parser.add_argument('-b', default=None, required=False)
    args = parser.parse_args()
    if args.a or args.b or args.c or args.e:
        args.path = args.path.split('-')[0]
        return args
    else:
        return None


def main():
    args = parse_arguments()
    if args:
        try:
            os.chdir(args.path)
            files_pattern = 'Murree_weather_*.txt'
            file_names = glob.glob(files_pattern)
            os.chdir("..")
            weather_report = WeatherReport(file_names)
            if args.e:
                weather_report.execute_first_task(args.e, args.path)
            if args.a:
                weather_report.execute_second_task(args.a, args.path)
            if args.c:
                weather_report.execute_third_task(args.c, args.path)
            if args.b:
                weather_report.execute_bonus_task(args.b, args.path)

        except FileNotFoundError:
            print('Files path is incorrect')
    else:
        print("usage: weatherman.py -dir /path/to/files [-option] [year/month] \n"
              "Options:\n"
              "e\tannual Report\n"
              "a\tMonthly Report\n"
              "c\tDaily Report\n"
              "b\tBonus")


if __name__ == "__main__":
    main()
