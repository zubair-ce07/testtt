
class EachDayReport:

    def __init__(self):
        self.maxTemp = 0
        self.minTemp = 0
        self.date = ''

    def printReport(self,weatherDict):
        if weatherDict["Max TemperatureC"] != '' and weatherDict["Min TemperatureC"] != '':
            self.maxTemp = int(weatherDict["Max TemperatureC"])
            self.minTemp = int(weatherDict["Min TemperatureC"])
            self.date = str(weatherDict["PKT"]).split("-")[2]
            if len(self.date) == 1:
                self.date = "0" + self.date

            print("\33[95m" + self.date,end=" ")
            print("\33[31m" + "+" * self.maxTemp,end=" ")
            print("\33[95m" + str(self.maxTemp) + "C")

            print("\33[95m" + self.date,end=" ")
            print("\33[94m" + "+" * self.minTemp,end=" ")
            print("\33[95m" + str(self.minTemp) + "C" + "\33[0m")