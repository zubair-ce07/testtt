import argparse
import calendar
from os.path import isfile, join
from os import listdir
import sys


def populate_year_dic_temp(HoldForYearDic, HoldForMonthDic, Month):
    HoldForYearDic.update({int(Month): HoldForMonthDic})
    HoldForMonthDic.clear()


def populate_year_dic(HoldForYearDic, HoldForMonthDic,
                      WeatherReport, Month, HoldYear):
    HoldForYearDic.update({Month: HoldForMonthDic})
    HoldForMonthDic.clear
    WeatherReport.dic.update({int(HoldYear): HoldForYearDic})
    HoldForYearDic.clear


def extract_month_weather_report(WeatherLine, HoldForMonthDic):
    WeatherLine = WeatherLine.split(',')
    WeatherLine[-1] = WeatherLine[-1].split('\n')[0]
    Date = int(WeatherLine[0].split('-')[-1])
    HoldForMonthDic.update({Date: WeatherLine})


class DataFromFiles:
    """
        Class for holding all the data from the Files
    """

    def __init__(self):
        self.dic = {}


# Parsing the data read from the file
class WeatherReportParse:
    """
        This class the parsing the data
        and populate it ir the object of
        DataFromFiles
    """

    def __init__(self, WeatherReport, WeatherFileNames):
        """
        This constructor is taking the extracted
        file names and the Data object and populate
        the Data.dic with the data in the files
        """

        HoldYear = 0
        HoldForMonthDic = {}
        HoldForYearDic = {}

        for File in WeatherFileNames:

            Year = File.split('_')[2]

            if HoldYear == 0:
                HoldYear = Year

            elif HoldYear == Year:
                populate_year_dic_temp(HoldForYearDic, HoldForMonthDic, Month)

            else:
                populate_year_dic(HoldForYearDic, HoldForMonthDic, WeatherReport, Month, HoldYear)

                if Year == "0000":
                    break
                HoldYear = Year

            Month = MonthToNumber[File.split('_')[-1].split('.')[0]]
            FileHandler = open("weatherfiles/weatherfiles/" + File)
            FileHandler.readline()

            for WeatherLine in FileHandler:
                extract_month_weather_report(WeatherLine, HoldForMonthDic)


class DataResults:
    """
        This class is holding the data analysis results
    """

    def __init__(self):
        self.HighestTemp = 0
        self.LowestTemp = 0
        self.MaxHumidity = 0
        self.HighestTempDate = 0
        self.LowestTempDate = 0
        self.MaxHumidityDate = 0
        self.AverageHighestTemp = 0
        self.AverageLowestTemp = 0
        self.AverageHumidity = 0

    def year_report(self, DataObj, Year):
        """
        This method is calculating the yearly result and populate the answers in the above variables
        """
        if Year not in DataObj.dic:
            return 0
        YearDic = DataObj.dic[Year]
        HighestTemp = -9999
        LowestTemp = 9999
        MaxHumidity = -9999
        HighestTempDate = 0
        LowestTempDate = 0
        MaxHumidityDate = 0

        for Month in YearDic:

            for Date in YearDic[Month]:

                if YearDic[Month][Date][1] != '' and int(YearDic[Month][Date][1]) > int(HighestTemp):
                    HighestTemp = YearDic[Month][Date][1]
                    HighestTempDate = YearDic[Month][Date][0]

                if YearDic[Month][Date][3] != '' and int(YearDic[Month][Date][3]) < int(LowestTemp):
                    LowestTemp = YearDic[Month][Date][3]
                    LowestTempDate = YearDic[Month][Date][0]

                if YearDic[Month][Date][7] != '' and int(YearDic[Month][Date][7]) > int(MaxHumidity):
                    MaxHumidity = YearDic[Month][Date][7]
                    MaxHumidityDate = YearDic[Month][Date][0]

        self.HighestTemp = HighestTemp
        self.LowestTemp = LowestTemp
        self.MaxHumidity = MaxHumidity
        self.HighestTempDate = HighestTempDate
        self.LowestTempDate = LowestTempDate
        self.MaxHumidityDate = MaxHumidityDate
        return 1

    def month_report(self, WeatherReport, Year, Month):

        """
                This method is calculating the second result and populate the answers in the above variables
        """
        if Year not in WeatherReport.dic or Month not in WeatherReport.dic[Year]:
            return 0

        MonthDic = WeatherReport.dic[Year][Month]
        count = [0, 0, 0]
        sum = [0, 0, 0]

        for Date in MonthDic:

            if MonthDic[Date][1] != '':
                count[0] += 1
                sum[0] += int(MonthDic[Date][1])

            if MonthDic[Date][3] != '':
                count[1] += 1
                sum[1] += int(MonthDic[Date][3])

            if MonthDic[Date][7] != '':
                count[2] += 1
                sum[2] += int(MonthDic[Date][7])

        self.AverageHighestTemp = sum[0] / count[0]
        self.AverageLowestTemp = sum[1] / count[1]
        self.AverageHumidity = sum[2] / count[2]

        return 1

    def show_year_result(self):
        """
                This method is showing the first result
        """
        print("Highest:", self.HighestTemp + "C on ",
              calendar.month_name[int(self.HighestTempDate.split('-')[1])],
              self.HighestTempDate.split('-')[2])

        print("Lowest:", self.LowestTemp + "C on ",
              calendar.month_name[int(self.LowestTempDate.split('-')[1])],
              self.LowestTempDate.split('-')[2])

        print("Humidity:", self.MaxHumidity + "% on ",
              calendar.month_name[int(self.MaxHumidityDate.split('-')[1])],
              self.MaxHumidityDate.split('-')[2], "\n\n\n")

    def show_month_result(self):
        """
                    This method is showing the second result
        """
        print("Highest Average:", str(self.AverageHighestTemp) + "C")
        print("Lowest Average:", str(self.AverageLowestTemp) + "C")
        print("Humidity Average:", str(self.AverageHumidity) + "% \n\n\n")


class DataReport:
    """
        This class is generating reports from the data
    """

    @staticmethod
    def show_seprate_graph(DataObj, Year, Month):
        """
                    This method is showing reports of the DataObj individually
        """
        if Year not in DataObj.dic or Month not in DataObj.dic[Year]:
            print("NA")
            return
        MonthDic = DataObj.dic[Year][Month]

        for Date in MonthDic:
            sys.stdout.write(MonthDic[Date][0].split('-')[-1])

            if MonthDic[Date][1] != '':

                for i in range(0, int(MonthDic[Date][1])):
                    sys.stdout.write(' + ')
                print(MonthDic[Date][1] + "C")

            else:
                print(" NA")
            sys.stdout.write(MonthDic[Date][0].split('-')[-1])

            if MonthDic[Date][3] != '':

                for i in range(0, int(MonthDic[Date][3])):
                    sys.stdout.write(' + ')
                print(MonthDic[Date][3] + "C")

            else:
                print(" NA")

        print("\n\n\n")

    @staticmethod
    def show_merge_graph(DataObj, Year, Month):
        """
                    This method is showing reports of the DataObj combinely
        """

        if Year not in DataObj.dic or Month not in DataObj.dic[Year]:
            print("NA")
            return

        MonthDic = DataObj.dic[Year][Month]

        for Date in MonthDic:
            low = 0
            high = 0
            sys.stdout.write(MonthDic[Date][0].split('-')[-1])

            if MonthDic[Date][1] != '':

                for i in range(0, int(MonthDic[Date][1])):
                    sys.stdout.write(' + ')
                high = MonthDic[Date][1] + "C"

            else:
                high = " NA"

            if MonthDic[Date][3] != '':

                for i in range(0, int(MonthDic[Date][3])):
                    sys.stdout.write(' * ')
                low = MonthDic[Date][3] + "C"

            else:
                low = " NA"

            print(high, "-", low)

        print("\n\n\n")


# Parsing Arguments
parser = argparse.ArgumentParser(description="Calculating and showing weather reports fetched from the data files")
parser.add_argument("ignore", type=str, help="Directory Destinantion")
parser.add_argument("-e", "--year", type=int, help="Year Parameter")
parser.add_argument("-a", "--month", type=str, help="Month Parameter")
parser.add_argument("-c", "--graphsingle", type=str, help="Show single graph")
parser.add_argument("-m", "--graphmerged", type=str, help="Show merged graph")
args = parser.parse_args()

Data = DataFromFiles()
MonthToNumber = {v: k for k, v in enumerate(
    calendar.month_abbr)}  # Creating a dictionary for converting the Month name to the Month Number
FileNames = [f for f in listdir("weatherfiles/weatherfiles/") if isfile(join("weatherfiles/weatherfiles/", f)) and f[
    0] != '.']  # Fetching all file names from the directory
FileNames.sort()

WeatherReportParse(Data, FileNames)
Results = DataResults()

if args.year:

    if Results.year_report(Data, args.year):
        Results.show_year_result()

    else:
        print(args.year," doesn't exist in the data")

if args.month:
    if Results.month_report(Data, int(args.month.split('/')[0]), int(args.month.split('/')[1])):
        Results.show_month_result()

    else:
        print(args.year," doesn't exist in the data")

if args.graphsingle:
    Report = DataReport()
    Report.show_seprate_graph(Data, int(args.graphsingle.split('/')[0]), int(args.graphsingle.split('/')[1]))

if args.graphmerged:
    Report = DataReport()
    Report.show_merge_graph(Data, int(args.graphmerged.split('/')[0]), int(args.graphmerged.split('/')[1]))

