from math import inf
import calendar
class YearReport:

    def __init__(self):
        self.maxTempDate = ""
        self.maxTemp = -inf
        self.minTempDate = ""
        self.minTemp = +inf
        self.maxHumidityDate = ""
        self.maxHumidity = -inf

    def setAccurateDate(self,weatherDict):
        if weatherDict["Max TemperatureC"] != '':
            if self.maxTemp < int(weatherDict["Max TemperatureC"]):
                self.maxTempDate = weatherDict["PKT"]
                self.maxTemp = int(weatherDict["Max TemperatureC"])
        if weatherDict["Min TemperatureC"] != '':    
            if self.minTemp > int(weatherDict["Min TemperatureC"]):
                self.minTempDate = weatherDict["PKT"]
                self.minTemp = int(weatherDict["Min TemperatureC"])
        if weatherDict["Max Humidity"] != '':    
            if self.maxHumidity < int(weatherDict["Max Humidity"]):
                self.maxHumidityDate = weatherDict["PKT"]
                self.maxHumidity = int(weatherDict["Max Humidity"])

    def printReport(self):
                            # Highest: 45C on June 23
                            # Lowest: 01C on December 22
                            # Humidity: 95% on August 14
        
        print("Highest: " + str(self.maxTemp) + "C " + "on " + str(self.dateFormat(self.maxTempDate)))
        print("Lowest: " + str(self.minTemp) + "C " + "on " + str(self.dateFormat(self.minTempDate)))
        print("Humidity: " + str(self.maxHumidity) + "% " + "on " + str(self.dateFormat(self.maxHumidityDate)))
        # print(self.maxTempDate)
        # print(self.minTempDate)
        # print(self.maxHumidityDate)

    def dateFormat(self,date):
        splitDate = date.split("-")
        return calendar.month_name[int(splitDate[1])] + " " + splitDate[2]