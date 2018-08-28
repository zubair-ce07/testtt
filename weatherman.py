from sys import argv
from yearReport import YearReport
from monthReport import MonthReport

if len(argv) == 4:
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
    #Task 1
    if "-e" in argv:
        yearReport = YearReport()
        for month in listOfMon:
            fullFileName = fileName + month + ".txt"
            try:
                fileReader = open(fullFileName).readlines()[1:]
                for line in fileReader:
                    print(line)
                    if len(line.strip()) == 16:
                        continue
                    zipList = zip(listofWeatherData,line.split(","))
                    dictOfWeather = dict(zipList)
                    yearReport.setAccurateDate(dictOfWeather)
                    dictOfWeather.clear()
            except FileNotFoundError:
                # print(fullFileName)
                continue
        yearReport.printReport()
    #Task 2
    elif "-a" in argv:
        monthReport = MonthReport()
        yearMonth = argv[3].split("/")
        fileName = argv[1] + "Murree_weather_" + yearMonth[0] + "_"
        try:
            fullFileName = fileName + listOfMon[int(yearMonth[1])-1] + ".txt"
        except IndexError:
            print("Month argument missing!")
            exit(1)
        # print(fullFileName)
        try:
            fileReader = open(fullFileName).readlines()[1:]
            for line in fileReader:
                if len(line.strip()) == 16:
                    continue
                zipList = zip(listofWeatherData,line.split(","))
                dictOfWeather = dict(zipList)
                monthReport.calSumOfData(dictOfWeather)
                dictOfWeather.clear()
        except FileNotFoundError:
            print("File Not Found")
        monthReport.takeAvgOfData()
        monthReport.printMonthReport()
    # Task3
    elif "-c" in argv:
        

else:
    print('Arguments missing')