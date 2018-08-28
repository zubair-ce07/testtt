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



    def cal_sum_of_data(self,weatherDict):
        if weatherDict["Max TemperatureC"] is not '':
            self.sumMaxTemp += int(weatherDict["Max TemperatureC"])
            self.maxTempCount += 1
        if weatherDict["Min TemperatureC"] is not '':
            self.sumMinTemp += int(weatherDict["Min TemperatureC"])
            self.minTempCount += 1
        if weatherDict["Max Humidity"] is not '':
            self.sumMeanHumidity += int(weatherDict["Mean Humidity"])
            self.meanHumidityCount += 1


    def take_avg_of_data(self):
        self.avgMaxTemp = self.sumMaxTemp // self.maxTempCount
        self.avgMinTemp = self.sumMinTemp // self.minTempCount
        self.avgMeanHumidity = self.sumMeanHumidity // self.meanHumidityCount

    def print_month_report(self):
        print("Highest Average: " + str(self.avgMaxTemp) + "C")
        print("Lowest Average: " + str(self.avgMinTemp) + "C")
        print("Average Mean Humidity: " + str(self.avgMeanHumidity) + "%")