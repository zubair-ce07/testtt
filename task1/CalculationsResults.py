import WeatherDataExtractor
import ResultStorage

class CalculationsResults:
#making an object that contains all the data in the form of an array
    weatherDataObj = WeatherDataExtractor.WeatherDataExtractor(3,"2006")
    weatherData = weatherDataObj.read_all_files()


# find highest, lowest and most humid day for specified objects/days
    def calculateForGivenDays(self,requiredDays):
        lowestTemp, ltd = self.lowestTempInYear(requiredDays)
        highestTemp, htd = self.highestTempInYear(requiredDays)
        humidity, hd = self.mostHumidDayOfYear(requiredDays)
        return ResultStorage.ResultStorage(highestTemp,lowestTemp,humidity,htd,ltd,hd)

#return all days of all months of the given year whose data is available
    def monthsOfYear(self,year):
        requiredMonths = []
        for month in range(len(CalculationsResults.weatherData)): # reference of all the months of the required year are returned in an array
            if (CalculationsResults.weatherData[month].pkt[:4] == year):
                requiredMonths.append(month)
        return requiredMonths

#return all days of all months whose data is available
    def daysOfMonth(self,month, year):
        requiredDays = []
        for days in range(len(CalculationsResults.weatherData)): # reference of all the months of the required year are returned in an array
            if (CalculationsResults.weatherData[days].pkt == None):
                continue
            if ((CalculationsResults.weatherData[days].pkt[:4] == year) and (self.weatherData[days].pkt[5] == month) or (self.weatherData[days].pkt[5:7] == month) ):
                requiredDays.append(days)
        return requiredDays

#calculate average highest lowest temperature and mean humidity
    def avgCalculation(self,requiredDays):
        avgLowestTemp = self.avgLowestTemp(requiredDays)
        avgHighestTemp = self.avgHighestTemp(requiredDays)
        avgHumidity = self.avgMeanHumidity(requiredDays)
        return ResultStorage.ResultStorage(avgHighestTemp, avgLowestTemp, avgHumidity, None, None, None)

#return lowest temperature for given days
    def lowestTempInYear(self,requiredDays):
        if (requiredDays == []):
            return None
        minTemp = int(self.weatherData[requiredDays[0]].minTemperature)
        minTempDay = self.weatherData[requiredDays[0]].pkt
        for i in requiredDays:
            try:
                if (int(self.weatherData[i].minTemperature) < minTemp):
                    minTemp = int(self.weatherData[i].minTemperature)
                    minTempDay = self.weatherData[i].pkt
            except:
                continue
        return minTemp, self.toDate(minTempDay)

#return highest temperature for given days
    def highestTempInYear(self,requiredDays):
        if (requiredDays == []):
            return None
        maxTemp = int(self.weatherData[requiredDays[0]].maxTemperature)
        maxTempDay = self.weatherData[requiredDays[0]].pkt
        for i in requiredDays:
            try:
                if (int(self.weatherData[i].maxTemperature) > maxTemp):
                    maxTemp = int(self.weatherData[i].maxTemperature)
                    maxTempDay = self.weatherData[i].pkt
            except:
                continue
        return (maxTemp, self.toDate(maxTempDay))

#returns most humid day for given days
    def mostHumidDayOfYear(self,requiredDays):
        if (requiredDays == []):
            return None
        try:
            humiditiLevel = int(self.weatherData[requiredDays[0]].meanHumidity)
            mostHumidDay = self.weatherData[requiredDays[0]].pkt
        except:
            humiditiLevel = None
            mostHumidDay = None
        for i in requiredDays:
            try:
                newHumidityLevel = int(self.weatherData[i].meanHumidity)
            except:
                continue
            if ((newHumidityLevel > humiditiLevel) or (humiditiLevel == None)):
                humiditiLevel = int(self.weatherData[i].meanHumidity)
                mostHumidDay = self.weatherData[i].pkt
        return (humiditiLevel, self.toDate(mostHumidDay))

# Return average lowest temperature for given days
    def avgLowestTemp(self,requiredDays):
        if (requiredDays == []):
            return None
        sum = 0
        for i in requiredDays:
            try:
                sum += int(CalculationsResults.weatherData[i].minTemperature)
            except:
                continue
        return (sum/len(requiredDays))

# Return average highest temperature for given days
    def avgHighestTemp(self,requiredDays):
        if (requiredDays == []):
            return None
        sum = 0
        for i in requiredDays:
            try:
                sum += int(CalculationsResults.weatherData[i].maxTemperature)
            except:
                continue
        return (sum / len(requiredDays))

# Return average mean humidity for given days
    def avgMeanHumidity(self,requiredDays):
        if (requiredDays == []):
            return None
        sum = 0

        for i in requiredDays:
            try:
                sum += int(CalculationsResults.weatherData[i].meanHumidity)
            except:
                continue
        return (sum / len(requiredDays))

# Convert date in the form that include month name
    def toDate(self,pkt):
        month = ""
        day = ""
        if (pkt == None):
            return None
        if (pkt[6] != "-"):
            if pkt[5:7] == '10':
                month = "Oct"
            elif pkt[5:7] == '11':
                month = "Nov"
            elif pkt[5:7] == '12':
                month = "Dec"
            day = pkt[8:]
        else:
            if pkt[5] == '1':
                month = "Jan"
            elif pkt[5] == '2':
                month = "Feb"
            elif pkt[5] == '3':
                month = "Mar"
            elif pkt[5] == '4':
                month = "Apr"
            elif pkt[5] == '5':
                month = "May"
            elif pkt[5] == '6':
                month = "Jun"
            elif pkt[5] == '7':
                month = "Jul"
            elif pkt[5] == '8':
                month = "Aug"
            elif pkt[5] == '9':
                month = "Sep"
            day = pkt[7:]
        return (month + " " + day)

