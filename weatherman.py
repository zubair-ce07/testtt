from sys import argv
from WmTask1 import WmTask1

if len(argv) == 4 and "-e" in argv:
    # print("Task1")
    fileName = argv[1] + "Murree_weather_" + argv[3] + "_"
    # print(fileName)

    listOfMon = ["Jan", "Feb", "Mar", "Apr", "May",
                 "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    listofWeatherData = ["PKT","Max TemperatureC","Mean TemperatureC","Min TemperatureC",
                        "Dew PointC","MeanDew PointC","Min DewpointC","Max Humidity", "Mean Humidity", 
                        "Min Humidity", "Max Sea Level PressurehPa", "Mean Sea Level PressurehPa", 
                        "Min Sea Level PressurehPa", "Max VisibilityKm", "Mean VisibilityKm", "Min VisibilitykM", 
                        "Max Wind SpeedKm/h", "Mean Wind SpeedKm/h", "Max Gust SpeedKm/h","PrecipitationCm",
                         "CloudCover", "Events","WindDirDegrees"]
    x = WmTask1()
    for month in listOfMon:
        fullFileName = fileName + month + ".txt"
        try:
            fileReader = open(fullFileName).readlines()[2:]
            for line in fileReader:
                if len(line.strip()) == 16:
                    continue
                zipList = zip(listofWeatherData,line.split(","))
                dictOfWeather = dict(zipList)
                x.setAccurateDate(dictOfWeather)
                dictOfWeather.clear()
        except FileNotFoundError:
            # print(fullFileName)
            continue
    x.printReport()
else:
    print('No')