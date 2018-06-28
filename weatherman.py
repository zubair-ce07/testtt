import sys
import os
from weather import Parser, Presenter, Calculator


def main():
    # Get all contents of the directory passed as the first argument

    if not len(sys.argv) % 2 == 0:
        print('Invalid Number of arguments')
        print('Sample Usage: python3 weatherman.py "path/to/dir" -e 2012')
        return

    if not os.path.exists(sys.argv[1]):
        print('Invalid Directory Path')
        return

    contents = os.listdir(sys.argv[1])
    contents = [os.path.join(sys.argv[1], x) for x in contents]

    # Remove nested directories and only pickup non hidden files

    files = [x for x in contents if os.path.isfile(
        x) and 'weather' in x and not x.startswith('.')]

    if len(files) == 0:
        print('No valid files found in directory')
        return

    # Read all files and extract data

    parser = Parser()

    weather_data = parser.read(files)

    # Remove Extra attributes and empty rows

    clean_data = parser.clean(weather_data)

    # Convert the data into easily readable form

    organized_data = parser.organize_data(clean_data)

    # for x in organizedData:
    #     print(x)

    # for x in organizedData:
    #     print(x['Mean Temp'] == '')

    # Perform Calculations according to the parameters given

    calculator = Calculator()
    mode = []
    result = []

    [mode.append(x) for x in sys.argv if x[0] == '-' and len(x) == 2]

    for m in mode:
        if '-a' == m:
            date = sys.argv[sys.argv.index('-a') + 1]
            date = date.split('/')

            if not len(date) == 2:
                print('Month not specified for', m)
                return

            year = date[0]
            month = date[1]

            if str.isdigit(year) and str.isdigit(month):
                month = str(int(month))
                result.append(calculator.calculate_monthly_average_report(
                    organized_data, year, month))
            else:
                print('Invalid Arguments')
                return

        if '-b' == m:
            date = sys.argv[sys.argv.index('-b') + 1]
            date = date.split('/')

            if not len(date) == 2:
                print('Month not specified for', m)
                return

            year = date[0]
            month = date[1]

            if str.isdigit(year) and str.isdigit(month):
                month = str(int(month))
                result.append(calculator.calculate_daily_extremes_report(
                    organized_data, year, month))
            else:
                print('Invalid Arguments')
                return

        if '-c' == m:
            date = sys.argv[sys.argv.index('-c') + 1]
            date = date.split('/')

            if not len(date) == 2:
                print('Month not specified for', m)
                return

            year = date[0]
            month = date[1]

            if str.isdigit(year) and str.isdigit(month):
                month = str(int(month))
                result.append(calculator.calculate_daily_extremes_report(
                    organized_data, year, month))
            else:
                print('Invalid Arguments')
                return
            pass

        if '-e' == m:
            year = sys.argv[sys.argv.index('-e') + 1]

            if str.isdigit(year):
                result.append(calculator.calculate_annual_result(
                    organized_data, year))
            else:
                print('Invalid Arguments')
                return

        sys.argv.pop(sys.argv.index(m))

    # print(result)

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
