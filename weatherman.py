import calendar
import os
import argparse
from datetime import datetime
import csv
from termcolor import colored

class WeatherReport:
    Data = []
    MaxList = []
    MinList = []
    Highest = 0
    Lowest = 0
    Humidity = 0

    HighestTempDate = None
    LowestTempDate = None
    HumidityTempDate = None

    def __init__(self, DataLst):
        self.Data = DataLst

    def SetMaxList(self):   #creates a dictionary with key=date and value = Max temperature
        self.MaxList = {x['PKT']: int(x['Max TemperatureC']) for x in self.Data if x['Max TemperatureC'] not in (None, '')}

    def SetMinList(self):   #creates a dictionary with key=date and value = Min temperature
        self.MinList = {x['PKT']: int(x['Min TemperatureC']) for x in self.Data if x['Min TemperatureC'] not in (None, '')}

class MonthlyReport(WeatherReport):
    def __init__(self, DataLst):
        WeatherReport.__init__(self,DataLst)

    def CalculateStatistics(self):
        self.SetMaxList()
        self.SetMinList()
        self.Highest = sum([i for i in self.MaxList.values()])/len(self.MaxList)    #calculating highest temperature average
        self.Lowest = sum([i for i in self.MinList.values()])/len(self.MinList)     #calculating lowest temperature average
        MeanHumList = [int(x[' Mean Humidity']) for x in self.Data if x[' Mean Humidity'] not in (None, '')]  #creating list of mean humidity column
        self.Humidity = sum(i for i in MeanHumList)/len(MeanHumList)    #calculating an average of mean temperatures

    def DisplayReport(self):
        print("Highest Average: {0}{1}".format(self.Highest,"C"))
        print("Lowest Average: {0}{1}".format(self.Lowest,"C"))
        print("Average Mean Humidity: {0}{1}".format(self.Humidity,"%"))

def MonthDay(TempDate): #for returning string of format: "MONTH_NAME DAY" for report displaying

    month = calendar.month_name[datetime.strptime(TempDate, '%Y-%m-%d').month]
    day = str(datetime.strptime(TempDate, '%Y-%m-%d').day)
    return month+" "+ day

class YearlyReport(WeatherReport):
    def __init__(self, DataLst):
        WeatherReport.__init__(self,DataLst)

    def CalculateStatistics(self):

        self.SetMaxList()
        self.SetMinList()

        self.HighestTempDate = max(self.MaxList, key=self.MaxList.get)  #setting date with highest temperature of year
        self.Highest = self.MaxList[self.HighestTempDate]   #setting highest temperature of year

        self.LowestTempDate = min(self.MinList, key=self.MinList.get)   #setting date with lowest temperature of year
        self.Lowest = self.MinList[self.LowestTempDate]     #setting lowest temperature of year

        MaxHumList = {x['PKT']: int(x['Max Humidity']) for x in self.Data if x['Max Humidity'] not in (None, '')}
        self.HumidityTempDate = max(MaxHumList, key=MaxHumList.get)     #setting date with highest humidity of year
        self.Humidity = MaxHumList[self.HumidityTempDate]   #setting highest humidity of year

    def DisplayReport(self):

        print("Highest: {0}{1} on {2}".format(self.Highest,'C',MonthDay(self.HighestTempDate)))
        print("Lowest: {0}{1} on {2}".format(self.Lowest, 'C', MonthDay(self.LowestTempDate)))
        print("Humidity: {0}{1} on {2}".format(self.Humidity, 'C', MonthDay(self.HumidityTempDate)))

class MonthlyBarChartReport(WeatherReport):
    def __init__(self, DataLst):
        WeatherReport.__init__(self,DataLst)

    def CalculateStatistics(self):
        #creating dict with key=date, values=Max temperature, Min temperature
        self.Data = {datetime.strptime(x['PKT'],'%Y-%m-%d').day: (int(x['Max TemperatureC']), int(x['Min TemperatureC']))
                    for x in self.Data if x['Max TemperatureC'] not in (None,'') }

    def DisplayReport(self):

        for day, temp in self.Data.items():
            print(day, end='')
            for i in range(0, temp[0]):
                print(colored('+', 'red'), end='')

            print("{0}{1}{2}{day_}".format(temp[0],'C','\n',day_=day), end ='')

            for i in range(0, temp[1]):
                print(colored('+', 'blue'), end='')

            print("{0}{1}".format(temp[1],'C'))

class SingleLineMonthlyReport(MonthlyBarChartReport):
    def __init__(self, DataLst):
        MonthlyBarChartReport.__init__(self,DataLst)

    def DisplayReport(self):
        for day, temp in self.Data.items():
            print(day, end='')
            for i in range(0, temp[1]):
                print(colored('+', 'blue'), end='')
            for i in range(0, temp[0]):
                print(colored('+', 'red'), end='')

            print("{0}{1}-{2}{1}".format(temp[1],"C",temp[0]))

def FetchArguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("FilePath", help = "Path to file directory", type = str)
    parser.add_argument('-e', help = 'Yearly Weather Report', type = lambda d: datetime.strptime(d, '%Y').strftime('%Y'))
    parser.add_argument('-a', help = 'Monthly Weather Report', type=lambda d: datetime.strptime(d, '%Y/%m'))
    parser.add_argument('-c', help = 'Monthly Weather Report display Bar Chart', type=lambda d: datetime.strptime(d, '%Y/%m'))
    parser.add_argument('-s', help='Single Line Monthly Weather Report display Bar Chart',type=lambda d: datetime.strptime(d, '%Y/%m'))

    args = parser.parse_args()

    return (args)

def IterateDirectory(criteria):     #criteria = commandline argument passed e.g. year

    data = []
    for each in os.listdir(args.FilePath):
        if criteria in each:
            with open(os.path.join(args.FilePath,each)) as csvfile:
                reader = csv.DictReader(csvfile)
                for each in reader:
                    data.append(each)

    return data #data contains a list of dictionaries where each dict represent one row of csv file of matching criteria

def YearMonConcat(year_month):  #for making string of format: "YEAR_MONTH ABRVIATION" for searching string in file name
    year = year_month.strftime('%Y')
    month = year_month.strftime('%m')
    return (year + '_' + calendar.month_abbr[int(month)])

def BuildReport(args):

    reports_list = []
    if (args.e is not None):
        data_list = IterateDirectory(args.e)
        rep = YearlyReport(data_list)
        reports_list.append(rep)

    if (args.a is not None):
        year_month = YearMonConcat(args.a)
        data_list = IterateDirectory(year_month)
        rep = MonthlyReport(data_list)
        reports_list.append(rep)

    if (args.c is not None):
        year_month = YearMonConcat(args.c)
        data_list = IterateDirectory(year_month)
        rep = MonthlyBarChartReport(data_list)
        reports_list.append(rep)

    if (args.s is not None):
        year_month = YearMonConcat(args.s)
        data_list = IterateDirectory(year_month)
        rep = SingleLineMonthlyReport(data_list)
        reports_list.append(rep)

    for obj in reports_list:
        obj.CalculateStatistics()
        obj.DisplayReport()
        print('\n')

if __name__ == '__main__':

    args = FetchArguments()
    BuildReport(args)




