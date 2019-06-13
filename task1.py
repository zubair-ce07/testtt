import calendar
import sys

from os import listdir
from os.path import isfile, join


class DataFromFiles:
    """
        Class for holding all the data from the Files
    """

    def __init__(self):
        self.dic = {}


# Parsing the data read from the file
class FileDataParsing:
    """
        This class the parsing the data and populate it ir the object of DataFromFiles
    """

    def __init__(self, DataObj, FileNamesList):
        """
        This constructor is taking the extracted file names and the
        Data object and populate the Data.dic with the data in the files
        """

        HoldYear = 0
        HoldForMonthDic = {}
        HoldForYearDic = {}
        for File in FileNamesList:
	
            Year = File.split('_')[2]
            if HoldYear == 0:
                HoldYear = Year
            elif HoldYear == Year:
                HoldForYearDic.update({int(Month): HoldForMonthDic})
                HoldForMonthDic = {}
            else:

                HoldForYearDic.update({Month: HoldForMonthDic})
                HoldForMonthDic = {}
                DataObj.dic.update({int(HoldYear): HoldForYearDic})
                HoldForYearDic = {}
                if Year == "0000":
                    break
                HoldYear = Year

            Month = MonthToNumber[File.split('_')[-1].split('.')[0]]
            FileHandler = open("weatherfiles/weatherfiles/" + File)
            FileHandler.readline()
            for WeatherLine in FileHandler:
                WeatherLine = WeatherLine.split(',')
                WeatherLine[-1] = WeatherLine[-1].split('\n')[0]
                Date = int(WeatherLine[0].split('-')[-1])
                HoldForMonthDic.update({Date: WeatherLine})


class DataResults:
    """
        This class is holding the data analysis results
    """

    def __init__(self):
        self.HighestTemp = 0
        self.LowestTemp = 0
        self.MaxHumidity = 0
        self.AverageHighestTemp = 0
        self.AverageLowestTemp = 0
        self.AverageHumidity = 0

    def res1(self, DataObj, Year):
        """
        This method is calculating the first result and populate the answers in the above variables
        """
        if Year not in DataObj.dic:
            return 0
        YearDic = DataObj.dic[Year]
        HighestTemp = [0, -9999]
        LowestTemp = [0, 0, 0, 9999]
        MaxHumidity = [0, 0, 0, 0, 0, 0, 0, -9999]

        for Month in YearDic:
            for Date in YearDic[Month]:
                if YearDic[Month][Date][1] != '' and int(YearDic[Month][Date][1]) > int(HighestTemp[1]):
                    HighestTemp = YearDic[Month][Date]
                if YearDic[Month][Date][3] != '' and int(YearDic[Month][Date][3]) < int(LowestTemp[3]):
                    LowestTemp = YearDic[Month][Date]
                if YearDic[Month][Date][7] != '' and int(YearDic[Month][Date][7]) > int(MaxHumidity[7]):
                    MaxHumidity = YearDic[Month][Date]

        self.HighestTemp = HighestTemp
        self.LowestTemp = LowestTemp
        self.MaxHumidity = MaxHumidity
        return 1

    def res2(self, DataObj, Year, Month):

        """
                This method is calculating the second result and populate the answers in the above variables
        """
        if Year not in DataObj.dic or Month not in DataObj.dic[Year]:
            return 0

        MonthDic = DataObj.dic[Year][Month]
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

    def show_result_1(self):
        """
                This method is showing the first result
        """
        print("Highest:", self.HighestTemp[1] + "C on ",
              calendar.month_name[int(self.HighestTemp[0].split('-')[1])],
              self.HighestTemp[0].split('-')[2])
        print("Lowest:", self.LowestTemp[3] + "C on ", calendar.month_name[int(self.LowestTemp[0].split('-')[1])],
              self.LowestTemp[0].split('-')[2])
        print("Humidity:", self.MaxHumidity[7] + "% on ",
              calendar.month_name[int(self.MaxHumidity[0].split('-')[1])],
              self.MaxHumidity[0].split('-')[2], "\n\n\n")

    def show_result_2(self):
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
    def show_report(DataObj, Year, Month):
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
    def merge_report(DataObj, Year, Month):
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


Data = DataFromFiles()
MonthToNumber = {v: k for k, v in enumerate(
    calendar.month_abbr)}  # Creating a dictionary for converting the Month name to the Month Number
FileNames = [f for f in listdir("weatherfiles/weatherfiles/") if isfile(join("weatherfiles/weatherfiles/", f)) and f[0] != '.']  # Fetching all file names from the directory

FileNames.sort()
FileNames.append("Dummy_Dummy_0000_Dummy")  # Act as delimeter

FileDataParsing(Data, FileNames)
Results = DataResults()
flags = []
years = []
for i in range(2, len(sys.argv), 2):
    flags.append(sys.argv[i])
    years.append(sys.argv[i + 1])

for i in range(0, len(flags)):

    if flags[i] == "-e":
        if Results.res1(Data, int(years[i])):
            Results.show_result_1()
        else:
            print("NA")
    elif flags[i] == "-a":
        if Results.res2(Data, int(years[i].split('/')[0]), int(years[i].split('/')[1])):
            Results.show_result_2()
        else:
            print("NA")

    elif flags[i] == "-c":
        Report = DataReport()
        Report.show_report(Data, int(years[i].split('/')[0]), int(years[i].split('/')[1]))

    elif flags[i] == "-b":
        Report = DataReport()
        Report.merge_report(Data, int(years[i].split('/')[0]), int(years[i].split('/')[1]))
