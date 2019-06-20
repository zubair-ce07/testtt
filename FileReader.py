import os
import WeatherReadings
import csv


class FileReader:

    allDataObjects = [] #all the data in objects is stored in this array

#Read file as dictionary object and stored required data values in the weatherReading object
    def readAllFiles(self):
        for i in os.listdir("weatherfiles"):
            try:
                csvFile = csv.DictReader(open("weatherfiles/%s" % i))
                for row in csvFile:
                    try:
                        pkt = row['PKT']
                    except:
                        continue
                    try:
                        maxTemp = row["Max TemperatureC"]
                    except:
                        maxTemp = None
                    try:
                        minTemp = row["Min TemperatureC"]
                    except:
                        minTemp = None
                    try:
                        avgTemp = row["Mean TemperatureC"]
                    except:
                        avgTemp = None
                    try:
                        maxHumidity = row["Max Humidity"]
                    except:
                        maxHumidity = None
                    try:
                        minHumidity = row[" Min Humidity"]
                    except:
                        minHumidity = None
                    try:
                        avgHumidity = row[" Mean Humidity"]
                    except:
                        avgHumidity = None
                    FileReader.storeData(pkt,maxTemp,minTemp,avgTemp,maxHumidity,minHumidity,avgHumidity)
            except:
                continue

# Store data in the data structure made for storing the weather data
    def storeData(pkt,maxTemp,minTemp,avgTemp,maxHumidity,minHumidity,avgHumidity):
        weatherDataObject = WeatherReadings.WeatherReadings(pkt,maxTemp,avgTemp,minTemp,maxHumidity,avgHumidity,minHumidity)
        FileReader.allDataObjects.append(weatherDataObject)


    def getAllData(self):
        return self.allDataObjects

