import os
import WeatherReadings

class FileReader:

    allDataObjects = [] #all the data in objects is stored in this array

    def readAllFiles(self):

        for i in os.listdir("weatherfiles"):
            try:
                file = open("weatherfiles/%s"%i, "r")
                fileDataArray = file.readlines()
                FileReader.splitData(fileDataArray[1:]) #reading the file per line
                file.close()
            except:
                continue
        print(FileReader.allDataObjects)

    def splitData(fileDataArray): # spliting each line in array format
        for i in fileDataArray:
            perDayData = i.split(",")
            FileReader.storeData(perDayData)


    def storeData(perDayData):
        obj = WeatherReadings.WeatherReading(perDayData) #storing those values in the form of an object
        FileReader.allDataObjects.append(obj)
        print(obj.maxTemperature)


check = FileReader()
check.readAllFiles()
