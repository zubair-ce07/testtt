
class WeatherReading: # Class to store data

    def __init__(self,weatherDataArray):
        self.pkt = weatherDataArray[0]
        self.maxTemperature = weatherDataArray[1]
        self.meanTemperature = weatherDataArray[2]
        self.minTemperature = weatherDataArray[3]
        self.dewPoint = weatherDataArray[4]
        self.meanDewPoint = weatherDataArray[5]
        self.minDewpoint = weatherDataArray[6]
        self.maxHumidity = weatherDataArray[7]
        self.meanHumidity = weatherDataArray[8]
        self.minHumidity = weatherDataArray[9]
        self.maxSeaLevelPressure = weatherDataArray[10]
        self.meanSeaLevelPressure = weatherDataArray[11]
        self.minSeaLevelPressure = weatherDataArray[12]
        self.maxVisibility = weatherDataArray[13]
        self.meanVisibility = weatherDataArray[14]
        self.minVisibility = weatherDataArray[15]
        self.maxWindSpeed = weatherDataArray[16]
        self.meanWindSpeed = weatherDataArray[17]
        self.maxGustSpeed = weatherDataArray[18]
        self.precipitation = weatherDataArray[19]
        self.cloudCover = weatherDataArray[20]
        self.events = weatherDataArray[21]
        self.windDirDegrees = weatherDataArray[22]


