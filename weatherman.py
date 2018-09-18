from sys import argv
import calendar
from year_report import YearReport
from month_report import MonthReport
from eachday_report import EachDayReport

if len(argv) == 4 or len(argv) == 8:
    listOfMon = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
        "Aug", "Sep", "Oct", "Nov", "Dec"
        ]

    listofWeatherData = [
        "PKT", "Max TemperatureC", "Mean TemperatureC", "Min TemperatureC",
        "Dew PointC", "MeanDew PointC", "Min DewpointC", "Max Humidity",
        "Mean Humidity", "Min Humidity", "Max Sea Level PressurehPa",
        "Mean Sea Level PressurehPa", "Min Sea Level PressurehPa",
        "Max VisibilityKm", "Mean VisibilityKm", "Min VisibilitykM",
        "Max Wind SpeedKm/h", "Mean Wind SpeedKm/h", "Max Gust SpeedKm/h",
        "PrecipitationCm", "CloudCover", "Events", "WindDirDegrees"
        ]
    # Task 1
    if "-e" in argv:
        fileName = argv[1] + "Murree_weather_" + argv[argv.index("-e")+1] + "_"
        year_report = YearReport()
        for month in listOfMon:
            fullFileName = fileName + month + ".txt"
            try:
                fileReader = open(fullFileName).readlines()[1:]
                for line in fileReader:
                    if len(line.strip()) == 16:
                        continue
                    zipList = zip(listofWeatherData, line.split(","))
                    dictOfWeather = dict(zipList)
                    year_report.set_accurate_date(dictOfWeather)
                    dictOfWeather.clear()
            except FileNotFoundError:
                continue
        print(
            "----------Weather Report of " + argv[argv.index("-e")+1] +
            "-----------"
            )
        year_report.print_year_report()

    # Task 2
    if "-a" in argv:
        month_report = MonthReport()
        yearMonth = argv[argv.index("-a")+1].split("/")
        fileName = argv[1] + "Murree_weather_" + yearMonth[0] + "_"
        try:
            fullFileName = fileName + listOfMon[int(yearMonth[1])-1] + ".txt"
        except IndexError:
            print("Month argument missing!")
            exit(1)
        try:
            fileReader = open(fullFileName).readlines()[1:]
            for line in fileReader:
                if len(line.strip()) == 16:
                    continue
                zipList = zip(listofWeatherData, line.split(","))
                dictOfWeather = dict(zipList)
                month_report.cal_sum_of_data(dictOfWeather)
                dictOfWeather.clear()
        except FileNotFoundError:
            print("File Not Found")
        month_report.take_avg_of_data()
        print(
            "--------------Weather Report of " +
            calendar.month_name[int(yearMonth[1])] + " " +
            yearMonth[0] + "-----------------"
            )
        month_report.print_month_report()

    # Task3
    if "-c" in argv:
        each_day_report = EachDayReport()
        yearMonth = argv[argv.index("-c")+1].split("/")
        fileName = argv[1] + "Murree_weather_" + yearMonth[0] + "_"
        try:
            fullFileName = fileName + listOfMon[int(yearMonth[1])-1] + ".txt"
        except IndexError:
            print("Month argument missing!")
            exit(1)
        print(
            "--------------Each day weather Report of " +
            calendar.month_name[int(yearMonth[1])] +
            " " + yearMonth[0] + "-----------------"
            )
        try:
            fileReader = open(fullFileName).readlines()[1:]
            for line in fileReader:
                if len(line.strip()) == 16:
                    continue
                zipList = zip(listofWeatherData, line.split(","))
                dictOfWeather = dict(zipList)
                each_day_report.print_eachday_report(dictOfWeather)
                # each_day_report.print_eachday_report_bonus(dictOfWeather)
                dictOfWeather.clear()
        except FileNotFoundError:
            print("File Not Found")

else:
    print('Arguments missing')
