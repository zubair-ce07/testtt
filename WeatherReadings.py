
class WeatherReadings: # Class to store data

    def __init__(self,pkt,maxTemperature,meanTemperature,minTemperature,maxHumidity,meanHumidity,minHumidity):
        self.pkt = pkt
        self.maxTemperature = maxTemperature
        self.meanTemperature = meanTemperature
        self.minTemperature = minTemperature
        self.maxHumidity = maxHumidity
        self.meanHumidity = meanHumidity
        self.minHumidity = minHumidity


