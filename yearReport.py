from math import inf

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
        if splitDate[1] == '01' or splitDate[1] == '1':
            return "January " + splitDate[2]
        elif splitDate[1] == '02' or splitDate[1] == '2':
            return "February " + splitDate[2]
        elif splitDate[1] == '03' or splitDate[1] == '3':
            return "March " + splitDate[2]
        elif splitDate[1] == '04' or splitDate[1] == '4':
            return "April " + splitDate[2]
        elif splitDate[1] == '05' or splitDate[1] == '5':
            return "May " + splitDate[2]
        elif splitDate[1] == '06' or splitDate[1] == '6':
            return "June " + splitDate[2]
        elif splitDate[1] == '07' or splitDate[1] == '7':
            return "July " + splitDate[2]
        elif splitDate[1] == '08' or splitDate[1] == '8':
            return "August " + splitDate[2]
        elif splitDate[1] == '09' or splitDate[1] == '9':
            return "September " + splitDate[2]
        elif splitDate[1] == '10':
            return "October " + splitDate[2]
        elif splitDate[1] == '11':
            return "November " + splitDate[2]
        elif splitDate[1] == '12':
            return "December " + splitDate[2]
        