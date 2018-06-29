import sys
import os
import operator
from colorsys import *


class WeatherReading:
    def __init__(self, PKT, MaxTemp, MeanTemp, MinTemp,
                 Dew, MeanDew, MinDew, MaxHumidity, MeanHumidity, MinHumidity,
                 MaxSeaPressure, MeanSeaPressure, MinSeaPressure,
                 MaxVisibility, MeanVisibility, Minvisibility, MaxWindSpeed,
                 MeanWindSpeed, MaxGustSpeed, Precipitation, CloudCover,
                 Events, WinDirDegrees):
        self.PKT = PKT
        self.MaxTemp = MaxTemp
        self.MeanTemp = MeanTemp
        self.MinTemp = MinTemp
        self.Dew = Dew
        self.MeanDew = MeanDew
        self.MinDew = MinDew
        self.MaxHumidity = MaxHumidity
        self.MeanHumidity = MeanHumidity
        self.MinHumidity = MinHumidity
        self.MaxSeaPressure = MaxSeaPressure
        self.MeanSeaPressure = MeanSeaPressure
        self.MinSeaPressure = MinSeaPressure
        self.MaxVisibility = MaxVisibility
        self.MeanVisibility = MeanVisibility
        self.Minvisibility = Minvisibility
        self.MaxWindSpeed = MaxWindSpeed
        self.MeanWindSpeed = MeanWindSpeed
        self.MaxGustSpeed = MaxGustSpeed
        self.Precipitation = Precipitation
        self.CloudCover = CloudCover
        self.Events = Events
        self.WinDirDegrees = WinDirDegrees


class ParseFiles:
    def __init__(self, filename):

        self.monthreadings = []

        try:

            with open(filename, "r") as filestream:
                next(filestream)
                for line in filestream:
                    currentline = line.split(",")
                    reading = WeatherReading(
                        currentline[0], currentline[1], currentline[2],
                        currentline[3], currentline[4], currentline[5],
                        currentline[6], currentline[7], currentline[8],
                        currentline[9], currentline[10], currentline[11],
                        currentline[12], currentline[13], currentline[14],
                        currentline[15], currentline[16], currentline[17],
                        currentline[18], currentline[19], currentline[20],
                        currentline[21], currentline[22]
                    )
                    if(currentline[1] != ''):
                        self.monthreadings.append(reading)

        except IOError:
            print("file does not exist")

    def __len__(self):
        length = 0
        for i in range(0, len(self.monthreadings)):
            length += 1
        return length

    def __getitem__(self, key):
        return self.monthreadings[key]


class CalculateMonthResults:
    def __init__(self, monthreadings):
        self.high_average = 0
        self.low_average = 0
        self.mean_humidity_average = 0


        highsum = 0
        lowsum = 0
        humiditysum = 0

        for i in range(0, len(monthreadings)):
            highsum += (int(monthreadings[i].MaxTemp))
            lowsum += (int(monthreadings[i].MinTemp))
            humiditysum += (int(monthreadings[i].MeanHumidity))

        if(len(monthreadings) != 0):
            high_average = float(highsum / len(monthreadings))
            low_average = float(lowsum / len(monthreadings))
            mean_humidity_average = float(humiditysum / len(monthreadings))
            
        print("Highest Average: " + str(high_average) + "C")
        print("Lowest Average: " + str(low_average) + "C")
        print("Average Mean Humidity: " + str(mean_humidity_average) + "%")


class Print_Month_Averages:
    def __init__(self, Month_Data):
        print("Highest Average: " + str(Month_Data.high_average) + "C")
        print("Lowest Average: " + str(Month_Data.low_average) + "C")
        print("Average Mean Humidity: " + str(Month_Data.mean_humidity_average) + "%")

class Print_Month_Bar:
    def __init__(self, monthreadings):

        Year, Month, Day = monthreadings[0].PKT.split("-")
        Month = MonthNames[int(Month) - 1]
        print(Month, Year)

        for i in range(0, len(monthreadings)):
            Max = int(monthreadings[i].MaxTemp)
            Min = int(monthreadings[i].MinTemp)
            high = str(i + 1)
            low = str(i + 1)
            
            high += ' '
            low += ' '
            
            for j in range(0, Max):
                high += "+"
            
            high += ' '
            high += str(Max)

            for j in range(0, Min):
                low += "+"
            
            low += ' '
            low += str(Min)

            print(high)
            print(low)
        
        

class CalculateYearResults:
    def __init__(self, YearReadings):
        self.highest = int(YearReadings[0][0].MaxTemp)
        self.lowest = int(YearReadings[0][0].MinTemp)
        self.humid = int(YearReadings[0][0].MaxHumidity)
        self.highest_date = 0
        self.lowest_date = 0
        self.humid_date = 0

        for i in range(0, len(YearReadings)):
            for j in range(0, len(YearReadings[i])):
                if(int(YearReadings[i][j].MaxTemp) > int(self.highest)):
                    self.highest = YearReadings[i][j].MaxTemp
                    self.highest_date = YearReadings[i][j].PKT
                
                if(int(YearReadings[i][j].MinTemp) < int(self.lowest)):
                    self.lowest = YearReadings[i][j].MinTemp
                    self.lowest_date = YearReadings[i][j].PKT
                
                if(int(YearReadings[i][j].MaxHumidity) > int(self.humid)):
                    self.humid = YearReadings[i][j].MaxHumidity
                    self.humid_date = YearReadings[i][j].PKT
        


class Print_Year_Results:
    def __init__(self, Highest, Lowest, Most_Humid, Highest_Date, Lowest_Date, Humid_Date):
        MonthNames = ['January', 'February', 'March', 'April', 'May',
              'June', 'July', 'August', 'September', 'October', 'November', 'December']
        High_Year, High_Month, High_Day = Highest_Date.split("-")
        Lowest_Year, Lowest_Month, Lowest_Day = Lowest_Date.split("-")
        Humid_Year, Humid_Month, Humid_Day = Humid_Date.split("-")
        
        High_Month = MonthNames[int(High_Month) - 1]
        Lowest_Month = MonthNames[int(Lowest_Month) - 1]
        Humid_Month = MonthNames[int(Humid_Month) - 1]

        print("Highest: " + str(Highest) + "C on " + str(High_Month) + " " + High_Day)
        print("Lowest: " + str(Lowest) + "C on " + str(Lowest_Month) + " " + Lowest_Day)
        print("Most Humidity: " + str(Most_Humid) + '% on' + str(Humid_Month) + " " + Humid_Day)


MonthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
              'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
filename = 'Murree_weather_'

option = 0
File_Data = []
MaxTemp_List = []
MinTemp_List = []
MaxHumidity_List = []
YearReadings = []

for i in range(2, len(sys.argv[1:]) + 1):

    word = sys.argv[i]

    if(word == '-a'):
        option = 1
    if(word == '-c'):
        option = 2
    if(word == '-e'):
        option = 3

    if("/" in word):
        year, month = word.split("/")
        filename = 'Murree_weather_'
        filename += (year + "_" + MonthNames[int(month) - 1] + ".txt")
        filename = sys.argv[1] + "/" + filename

#        print(filename)
        File_Data = (ParseFiles(filename))
        if(option == 1):
            Results = CalculateMonthResults(File_Data)
#           Print_Month_Averages(Results)
        elif(option == 2):
            Print_Month_Bar(File_Data.monthreadings)

    elif(len(word) > 2):
        for j in range(0, 12):
            filename = 'Murree_weather_'
            filename += (word + "_" + MonthNames[j] + ".txt")
            filename = sys.argv[1] + "/" + filename

#            print(filename)
            File_Data = (ParseFiles(filename))
            YearReadings.append(File_Data.monthreadings)

        YearResults = CalculateYearResults(YearReadings)
        Print_Year_Results(YearResults.highest, YearResults.lowest, YearResults.humid, YearResults.highest_date, YearResults.lowest_date, YearResults.humid_date)

#print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
