from sys import argv
import calendar
from yearReport import YearReport
from monthReport import MonthReport
from eachDayReport import EachDayReport

if len(argv) == 4 or len(argv) == 8:


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
        fileName = argv[1] + "Murree_weather_" + argv[argv.index("-e")+1] + "_"
        yearReport = YearReport()
        for month in listOfMon:
            fullFileName = fileName + month + ".txt"
            # print(fullFileName)
            try:
                fileReader = open(fullFileName).readlines()[1:]
                for line in fileReader:
                    # print(line)
                    if len(line.strip()) == 16:
                        continue
                    zipList = zip(listofWeatherData,line.split(","))
                    dictOfWeather = dict(zipList)
                    yearReport.setAccurateDate(dictOfWeather)
                    dictOfWeather.clear()
            except FileNotFoundError:
                # print(fullFileName)
                continue
        print("--------------Weather Report of " + argv[argv.index("-e")+1] + "-----------------")
        yearReport.printReport()
    #Task 2
    if "-a" in argv:
        monthReport = MonthReport()
        yearMonth = argv[argv.index("-a")+1].split("/")
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
        print("--------------Weather Report of "+ calendar.month_name[int(yearMonth[1])] + " " + yearMonth[0] + "-----------------")
        monthReport.printMonthReport()
    # Task3
    if "-c" in argv:
        eachDay = EachDayReport()
        yearMonth = argv[argv.index("-c")+1].split("/")
        fileName = argv[1] + "Murree_weather_" + yearMonth[0] + "_"
        try:
            fullFileName = fileName + listOfMon[int(yearMonth[1])-1] + ".txt"
        except IndexError:
            print("Month argument missing!")
            exit(1)
        # print(fullFileName)
        print("--------------Each day weather Report of "+ calendar.month_name[int(yearMonth[1])] + " " + yearMonth[0] + "-----------------")
        try:
            fileReader = open(fullFileName).readlines()[1:]
            for line in fileReader:
                if len(line.strip()) == 16:
                    continue
                zipList = zip(listofWeatherData,line.split(","))
                dictOfWeather = dict(zipList)
                eachDay.printReport(dictOfWeather)
                # eachDay.printReportBonus(dictOfWeather)
                dictOfWeather.clear()
        except FileNotFoundError:
            print("File Not Found")

else:
    print('Arguments missing')
