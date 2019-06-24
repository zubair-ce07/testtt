import WeatherDataExtractor
import ResultStorage
import calendar


class CalculationsResults:

    #weatherDataObj = WeatherDataExtractor.WeatherDataExtractor("2006", 4)
    #weatherData = weatherDataObj.read_all_files()

# find highest, lowest and most humid day for specified objects/days
    '''def calculateForGivenDays(self):
        lowestTemp, ltd = self.lowestTempInYear()
        highestTemp, htd = self.highestTempInYear()
        humidity, hd = self.mostHumidDayOfYear()
        return ResultStorage.ResultStorage(highestTemp,lowestTemp,humidity,htd,ltd,hd)

    def avgCalculation(self):
        avgLowestTemp = self.avgLowestTemp()
        avgHighestTemp = self.avgHighestTemp()
        avgHumidity = self.avgMeanHumidity()
        return ResultStorage.ResultStorage(avgHighestTemp, avgLowestTemp, avgHumidity, None, None, None)'''

#return lowest temperature for given days
    def lowestTempInYear(self,weatherData):
        try:
            minTemp = int(weatherData[0].minTemperature)
            minTempDay = weatherData[0].pk
        except:
            minTemp = None
            minTempDay = None
        for i in weatherData:
            try:
                if (int(i.minTemperature) < minTemp or (minTemp == None)):
                    minTemp = int(i.minTemperature)
                    minTempDay = i.pkt
            except:
                continue
        return minTemp, self.toDate(minTempDay)

#return highest temperature for given days
    def highestTempInYear(self,weatherData):
        try:
            maxTemp = int(weatherData[0].maxTemperature)
            maxTempDay = weatherData[0].pkt
        except:
            maxTemp = None
            maxTempDay = None
        for i in weatherData:
            try:
                if (int(i.maxTemperature) > maxTemp or maxTemp == None):
                    maxTemp = int(i.maxTemperature)
                    maxTempDay = i.pkt
            except:
                continue
        return (maxTemp, self.toDate(maxTempDay))

#returns most humid day for given days
    def mostHumidDayOfYear(self,weatherData):
        try:
            humiditiLevel = int(weatherData[0].meanHumidity)
            mostHumidDay = weatherData[0].pkt
        except:
            humiditiLevel = None
            mostHumidDay = None
        for i in weatherData:
            try:
                if ((int(i.meanHumidity) > humiditiLevel) or (humiditiLevel == None)):
                    humiditiLevel = int(i.meanHumidity)
                    mostHumidDay = i.pkt
            except:
                continue
        return (humiditiLevel, self.toDate(mostHumidDay))

# Return average lowest temperature for given days
    def avgLowestTemp(self,weatherData):
        sum = 0
        count = 0
        for i in weatherData:
            try:
                sum += int(i.minTemperature)
                count += 1
            except:
                continue
        return (sum/count)

# Return average highest temperature for given days
    def avgHighestTemp(self,weatherData):
        count = 0
        sum = 0
        for i in weatherData:
            try:
                sum += int(i.maxTemperature)
                count += 1
            except:
                continue

        return (sum / count)

# Return average mean humidity for given days
    def avgMeanHumidity(self,weatherData):
        count = 0
        sum = 0

        for i in weatherData:
            try:
                sum += int(i.meanHumidity)
                count += 1
            except:
                continue
        return (sum / count)

# Convert date in the form that include month name
    def toDate(self,pkt):
        if pkt == None:
            return None
        if (pkt[6] != "-"):
            month =  calendar.month_name[int(pkt[5:7])]
            day = pkt[8:]
        else:
            month = calendar.month_name[int(pkt[5])]
            day = pkt[7:]
        return (month[:3] + " " + day)

