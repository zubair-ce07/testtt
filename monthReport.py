from math import inf

class MonthReport:

    def __init__(self):
        self.sumMaxTemp = 0
        self.avgMaxTemp = 0
        self.maxTempCount = 0

        self.sumMinTemp = 0
        self.avgMinTemp = 0
        self.minTempCount = 0

        self.sumMeanHumidity = 0
        self.avgMeanHumidity = 0
        self.meanHumidityCount = 0



    def calSumOfData(self,weatherDict):
        if weatherDict["Max TemperatureC"] != '':
            # if self.maxAvgTemp < int(weatherDict["Max TemperatureC"]):
            self.sumMaxTemp += int(weatherDict["Max TemperatureC"])
            self.maxTempCount += 1
            # print(self.avgMaxTemp)
        if weatherDict["Min TemperatureC"] != '':
            # if self.minAvgTemp > int(weatherDict["Min TemperatureC"]):
            self.sumMinTemp += int(weatherDict["Min TemperatureC"])
            self.minTempCount += 1
            # print(weatherDict["Min TemperatureC"])
        if weatherDict["Max Humidity"] != '':
            # if self.maxAvgHumidity < int(weatherDict["Max Humidity"]):
            self.sumMeanHumidity += int(weatherDict["Mean Humidity"])
            self.meanHumidityCount += 1
            # print(weatherDict["Mean Humidity"])


    def takeAvgOfData(self):
        self.avgMaxTemp = self.sumMaxTemp // self.maxTempCount
        self.avgMinTemp = self.sumMinTemp // self.minTempCount
        self.avgMeanHumidity = self.sumMeanHumidity // self.meanHumidityCount

    def printMonthReport(self):
        print("Highest Average: " + str(self.avgMaxTemp) + "C")
        print("Lowest Average: " + str(self.avgMinTemp) + "C")
        print("Average Mean Humidity: " + str(self.avgMeanHumidity) + "%")