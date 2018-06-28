import sys
import os
from weatherModule import Parser, Presenter, Calculator


def main():
    # Get all contents of the directory passed as the first argument

    contents = os.listdir(sys.argv[1])
    contents = [os.path.join(sys.argv[1], x) for x in contents]

    # Remove nested directories and only pickup non hidden files

    files = [x for x in contents if os.path.isfile(
        x) and not x.startswith('.')]

    # Read all files and extract data

    parser = Parser()

    weatherData = parser.read(files)

    cleanData = parser.clean(weatherData)

    organizedData = parser.organizeData(cleanData)

    # for x in organizedData:
    #     print(x)

    # for x in organizedData:
    #     print(x['Mean Temp'] == '')

    # Perform Calculations

    calculator = Calculator()
    mode = []
    result = []

    [mode.append(x) for x in sys.argv if x[0] == '-']
    mode.sort()

    if '-a' in mode:
        date = sys.argv[sys.argv.index('-a') + 1]
        date = date.split('/')

        year = date[0]
        month = date[1]

        if str.isdigit(year) and str.isdigit(month):
            month = str(int(month))
            result.append(calculator.calculateMonthlyAverageReport(
                organizedData, year, month))
        pass

    if '-b' in mode:
        date = sys.argv[sys.argv.index('-b') + 1]
        date = date.split('/')

        year = date[0]
        month = date[1]

        if str.isdigit(year) and str.isdigit(month):
            month = str(int(month))
            result.append(calculator.calculateDailyExtremesReport(
                organizedData, year, month))
        pass

    if '-c' in mode:
        date = sys.argv[sys.argv.index('-c') + 1]
        date = date.split('/')

        year = date[0]
        month = date[1]

        if str.isdigit(year) and str.isdigit(month):
            month = str(int(month))
            result.append(calculator.calculateDailyExtremesReport(
                organizedData, year, month))
        pass

    if '-e' in mode:
        year = sys.argv[sys.argv.index('-e') + 1]

        if str.isdigit(year):
            result.append(calculator.calculateAnnualResult(
                organizedData, year))
        pass

    # print(result)

    presenter = Presenter()

    if len(mode) == len(result):
        print('No Error Occured In Computation\n')

        while len(mode) != 0:
            m = mode.pop()
            r = result.pop()

            if m == '-e':
                presenter.presentAnnualReport(r)
            elif m == '-a':
                presenter.presentMonthyAverageReport(r)
            elif m == '-b':
                presenter.presentDailyExtremesReport(r, horizontal=True)
            elif m == '-c':
                presenter.presentDailyExtremesReport(r)

            # print(m)
            # print(r)


if __name__ == "__main__":
    main()
