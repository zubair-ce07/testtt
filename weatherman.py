import sys
import glob
import os
import re
import calendar
from datetime import datetime
from termcolor import colored

class WeatherMan():
    def print_Yearly_results(self, filePath, year):

        fileNames = []
        os.chdir(filePath)
        for file in glob.glob("*.txt"):
            if file.find(year) != -1:
                fileNames.append(file)

        if len(fileNames) == 0:
            print('No File Found!')
        else:
            for fileName in fileNames:

                f = open(fileName, 'r')
                next(f)
                highTemp = {}
                lowTemp = {}
                highHumidity = {}

                for line in f:
                    splittedWords = line.split(',')
                    highTemp[splittedWords[0]] = splittedWords[1]
                    lowTemp[splittedWords[0]] = splittedWords[3]
                    highHumidity[splittedWords[0]] = splittedWords[7]

            def key_search(x):
                return x[1]

            highTempRes = sorted(
                highTemp.items(),
                key=key_search,
                reverse=True)
            lowTempRes = sorted(lowTemp.items(), key=key_search, reverse=True)
            highHumidityRes = sorted(
                highHumidity.items(),
                key=key_search,
                reverse=True)
            del highTempRes[1:]
            del lowTempRes[1:]
            del highHumidityRes[1:]
            highDate = datetime.strptime(highTempRes[0][0], '%Y-%m-%d')
            lowDate = datetime.strptime(lowTempRes[0][0], '%Y-%m-%d')
            humDate = datetime.strptime(highHumidityRes[0][0], '%Y-%m-%d')

            print ('Highest: ' + \
                  highTempRes[0][1] + \
                  'C on ' + \
                  highDate.strftime("%B") \
                  + ' ' + str(highDate.strftime("%d")))
            print ('Lowest: ' + lowTempRes[0][1] +\
                  'C on ' + lowDate.strftime("%B") +\
                  ' ' + str(lowDate.strftime("%d")))
            print ('Humidity: ' +\
                  highHumidityRes[0][1] +\
                  '% on ' + humDate.strftime("%B") +\
                  ' ' + str(humDate.strftime("%d")))

        return

    def verify_directory(self, directoryPath):
        if os.path.isdir(directoryPath):
            return True
        else:
            return False
        return

    def verify_year(self, year):
        if year.isdigit() and len(year) == 4:
            return True
        else:
            return False

        return

    def verify_year_month(self, yearMonth):
        match = re.search(r'^\d\d\d\d/\d+$', yearMonth)
        if match:
            splittedWords = yearMonth.split('/')
            month = int(splittedWords[1])
            if month >= 1 and month <= 12:
                return True
            else:
                return False
        else:
            return False

        return

    def print_month_average(self, filePath, year, month):

        fileNames = []
        os.chdir(filePath)
        for file in glob.glob("*.txt"):
            if file.find(year) != -1 and file.find(month) != -1:
                fileNames.append(file)

        if len(fileNames) == 0:
            print('No Data Found!')
        else:
            for fileName in fileNames:

                f = open(fileName, 'r')
                next(f)
                highTemp = {}
                lowTemp = {}
                highHumidity = {}

                for line in f:
                    splittedWords = line.split(',')
                    highTemp[splittedWords[0]] = splittedWords[1]
                    lowTemp[splittedWords[0]] = splittedWords[3]
                    highHumidity[splittedWords[0]] = splittedWords[9]

                    highTempAvg = self.find_average(highTemp.values())
                    lowTempAvg = self.find_average(lowTemp.values())
                    highHumAvg = self.find_average(highHumidity.values())

            print('Highest Average: ' + str(round(highTempAvg, 2)) + 'C')
            print('Lowest average: ' + str(round(lowTempAvg, 2)) + 'C')
            print('average Mean Humidity: ' + str(round(highHumAvg, 2)) + '%')
        return

    def find_average(self, values):
        sumVal = 0.0
        for val in values:
            if len(val) != 0:
                sumVal += float(val)
        return sumVal / len(values)

    def print_day_bars(self, filePath, year, month):

        fileNames = []
        os.chdir(filePath)
        for file in glob.glob("*.txt"):
            if file.find(year) != -1 and file.find(month) != -1:
                fileNames.append(file)

        if len(fileNames) == 0:
            print('No Data Found!')
        else:
            for fileName in fileNames:

                f = open(fileName, 'r')
                next(f)

                for line in f:
                    splittedWords = line.split(',')
                    day = datetime.strptime(splittedWords[0], '%Y-%m-%d')

                    high = self.get_Integer(splittedWords[1])
                    low = self.get_Integer(splittedWords[3])

                    """print(day.strftime("%d"),
                    self.print_plus(high,'red'))
                    print(str(high) + 'C')
                    print(day.strftime("%d"),
                    self.print_plus(low,'blue'))
                    print(str(low) + 'C')
                    """
                    #print(day.strftime("%d"), end=' ')
                    print(day.strftime("%d"),end="")
                    self.print_plus(low, 'blue')
                    self.print_plus(high - low, 'red')
                    print(str(low) + 'C - ' + str(high) + 'C')
        return

    def get_Integer(self, val):
        if len(val) == 0:
            result = 0
        else:
            result = int(val)

        return result

    def print_plus(self, val, color):
        i = 0
        while i < val:
            print(colored('+', color),end="")
            i += 1
        return


def sub_main(directoryPath, year, reportType):
    weather = WeatherMan()
    if reportType == '-e':
        if weather.verify_directory(directoryPath) and weather.verify_year(year):
            weather.print_Yearly_results(directoryPath, year)
        else:
            print('Incorrect Arguments!')

    elif reportType == '-a':

        if weather.verify_directory(
                directoryPath) and weather.verify_year_month(year):
            splittedWords = year.split('/')
            year = splittedWords[0]
            temp = calendar.month_name[int(splittedWords[1])]
            month = temp[0:3]
            weather.print_month_average(directoryPath, year, month)
        else:
            print("Incorrect Arguments!")

    elif reportType == '-c':

        if weather.verify_directory(
                directoryPath) and weather.verify_year_month(year):
            splittedWords = year.split('/')
            year = splittedWords[0]
            temp = calendar.month_name[int(splittedWords[1])]
            month = temp[0:3]
            weather.print_day_bars(directoryPath, year, month)
        else:
            print("Incorrect Arguments!")
    return


def main():
    if len(sys.argv) == 4:
        directoryPath = sys.argv[1]
        year = sys.argv[3]
        reportType = sys.argv[2]
        sub_main(directoryPath, year, reportType)
    elif len(sys.argv) == 8:
        directoryPath = sys.argv[1]
        year1 = sys.argv[3]
        year2 = sys.argv[5]
        year3 = sys.argv[7]
        reportType1 = sys.argv[2]
        reportType2 = sys.argv[4]
        reportType3 = sys.argv[6]
        sub_main(directoryPath, year1, reportType1)
        print('#########################################')
        sub_main(directoryPath, year2, reportType2)
        print('#########################################')
        sub_main(directoryPath, year3, reportType3)

    else:
        print('Incorrect arguments!')

    sys.exit(1)


if __name__ == '__main__':
    main()
