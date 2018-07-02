import os
from weather import Parser, Presenter, Calculator
import argparse


def main():
    # Get all contents of the directory passed as the first argument
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("-e", help=("For a given year display the highest temperature and day,"
                                    " lowest temperature and day, most humid day and humidity"),
                        action="append")
    parser.add_argument("-a", help=("For a given month display the average highest temperature,"
                                    " average lowest temperature,average mean humidity"),
                        action="append")
    parser.add_argument("-c",
                        help=("For a given month draw two horizontal bar charts on the console for the highest and"
                              " lowest temperature on each day. Highest in red and lowest in blue"),
                        action="append")
    parser.add_argument("-b", help=("For a given month draw one horizontal bar chart on the console for the highest"
                                    " and lowest temperature on each day. Highest in red and lowest in blue."),
                        action="append")
    args = parser.parse_args()

    if not os.path.exists(args.directory):
        print('Invalid Directory Path')
        return

    contents = os.listdir(args.directory)
    contents = [os.path.join(args.directory, x) for x in contents]

    # Remove nested directories and only pickup non hidden files

    files = [x for x in contents if os.path.isfile(
        x) and 'weather' in x and not x.startswith('.')]

    if len(files) == 0:
        print('No valid files found in directory')
        return

    # Read all files and extract data

    parser = Parser()

    weather_data = parser.read(files)

    # Convert the data into easily readable form and clean it

    organized_data = parser.clean(weather_data)

    # for x in organizedData:
    #     print(x)

    # for x in organizedData:
    #     print(x['Mean Temp'] == '')

    # Perform Calculations according to the parameters given

    calculator = Calculator()
    mode = []
    result = []

    if args.a:
        for arg in args.a:
            date = arg
            date = date.split('/')

            if not len(date) == 2:
                print('Month not specified for -a')
                return

            year = date[0]
            month = date[1]

            if str.isdigit(year) and str.isdigit(month):
                month = str(int(month))
                mode.append('-a')
                result.append(calculator.calculate_monthly_average_report(
                    organized_data, year, month))
            else:
                print('Invalid Arguments')
                return

    if args.b:
        for arg in args.b:
            date = arg
            date = date.split('/')

            if not len(date) == 2:
                print('Month not specified for -b')
                return

            year = date[0]
            month = date[1]

            if str.isdigit(year) and str.isdigit(month):
                month = str(int(month))
                mode.append('-b')
                result.append(calculator.calculate_daily_extremes_report(
                    organized_data, year, month))
            else:
                print('Invalid Arguments')
                return

    if args.c:
        for arg in args.c:
            date = arg
            date = date.split('/')

            if not len(date) == 2:
                print('Month not specified for -c')
                return

            year = date[0]
            month = date[1]

            if str.isdigit(year) and str.isdigit(month):
                month = str(int(month))
                mode.append('-c')
                result.append(calculator.calculate_daily_extremes_report(
                    organized_data, year, month))
            else:
                print('Invalid Arguments')
                return

    if args.e:
        for arg in args.e:
            year = arg

            if str.isdigit(year):
                mode.append('-e')
                result.append(calculator.calculate_annual_result(
                    organized_data, year))
            else:
                print('Invalid Arguments')
                return

    # Print the Calculation results

    presenter = Presenter()

    mode.reverse()
    result.reverse()

    if len(mode) == len(result):
        print('No Error Occurred In Computation\n')

        while len(mode) != 0:
            m = mode.pop()
            r = result.pop()

            print(m)
            # print(r)
            # print('\n\n')

            if m == '-e':
                presenter.present_annual_report(r)
            elif m == '-a':
                presenter.present_monthly_average_report(r)
            elif m == '-b':
                presenter.present_daily_extremes_report(r, horizontal=True)
            elif m == '-c':
                presenter.present_daily_extremes_report(r)
                pass

            # print(m)
            # print(r)


if __name__ == "__main__":
    main()
