"""This script use to run the waetherman app
it tasks command line arguments to differntiate
that wether it prints the YEAR,MONTH and DAY report"""
import sys
from sys import argv
import calendar
from year_report import YearReport
from month_report import MonthReport
from eachday_report import EachDayReport

if len(argv) == 4 or len(argv) == 8:
    MONTHS = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
        "Aug", "Sep", "Oct", "Nov", "Dec"
        ]

    DATA_COL = [
        "PKT", "Max TemperatureC", "Mean TemperatureC", "Min TemperatureC",
        "Dew PointC", "MeanDew PointC", "Min DewpointC", "Max Humidity",
        "Mean Humidity", "Min Humidity", "Max Sea Level PressurehPa",
        "Mean Sea Level PressurehPa", "Min Sea Level PressurehPa",
        "Max VisibilityKm", "Mean VisibilityKm", "Min VisibilitykM",
        "Max Wind SpeedKm/h", "Mean Wind SpeedKm/h", "Max Gust SpeedKm/h",
        "PrecipitationCm", "CloudCover", "Events", "WindDirDegrees"
        ]
    # Task 1
    """This below if handles the YearReport"""
    if "-e" in argv:
        FILE_NAME = argv[1] + "Murree_weather_"
        FILE_NAME = FILE_NAME + argv[argv.index("-e")+1] + "_"
        year_report = YearReport()
        FILE_READ = 0
        for month in MONTHS:
            FULL_FILE_NAME = FILE_NAME + month + ".txt"
            try:
                FILE_READER = open(FULL_FILE_NAME).readlines()[1:]
                for line in FILE_READER:
                    if len(line.strip()) == 16:
                        continue
                    zipList = zip(DATA_COL, line.split(","))
                    dictOfWeather = dict(zipList)
                    year_report.set_accurate_date(dictOfWeather)
                    dictOfWeather.clear()
                    FILE_READ += 1
            except FileNotFoundError:
                continue
        if FILE_READ == 0:
            print("No data found")
            sys.exit()
        print(
            "----------Weather Report of " + argv[argv.index("-e")+1] +
            "-----------"
            )
        year_report.print_year_report()

    # Task 2
    """This below if hanldes the monthly report"""
    if "-a" in argv:
        month_report = MonthReport()
        YEAR_MONTH = argv[argv.index("-a")+1].split("/")
        FILE_NAME = argv[1] + "Murree_weather_" + YEAR_MONTH[0] + "_"
        FILE_READ = 0
        try:
            FULL_FILE_NAME = FILE_NAME + MONTHS[int(YEAR_MONTH[1])-1] + ".txt"
        except IndexError:
            print("Month argument missing!")
            exit(1)
        try:
            FILE_READER = open(FULL_FILE_NAME).readlines()[1:]
            for line in FILE_READER:
                if len(line.strip()) == 16:
                    continue
                zipList = zip(DATA_COL, line.split(","))
                dictOfWeather = dict(zipList)
                month_report.cal_sum_of_data(dictOfWeather)
                dictOfWeather.clear()
                FILE_READ += 1
        except FileNotFoundError:
            print("File Not Found")
        if FILE_READ == 0:
            print("No data found")
            sys.exit()
        month_report.take_avg_of_data()
        print(
            "--------------Weather Report of " +
            calendar.month_name[int(YEAR_MONTH[1])] + " " +
            YEAR_MONTH[0] + "-----------------"
            )
        month_report.print_month_report()

    # Task3
    """This below if hanldes the eachday report"""
    if "-c" in argv:
        each_day_report = EachDayReport()
        YEAR_MONTH = argv[argv.index("-c")+1].split("/")
        FILE_NAME = argv[1] + "Murree_weather_" + YEAR_MONTH[0] + "_"
        FILE_READ = 0
        try:
            FULL_FILE_NAME = FILE_NAME + MONTHS[int(YEAR_MONTH[1])-1] + ".txt"
        except IndexError:
            print("Month argument missing!")
            exit(1)
        print(
            "--------------Each day weather Report of " +
            calendar.month_name[int(YEAR_MONTH[1])] +
            " " + YEAR_MONTH[0] + "-----------------"
            )
        try:
            FILE_READER = open(FULL_FILE_NAME).readlines()[1:]
            for line in FILE_READER:
                if len(line.strip()) == 16:
                    continue
                zipList = zip(DATA_COL, line.split(","))
                dictOfWeather = dict(zipList)
                each_day_report.print_eachday_report(dictOfWeather)
                # each_day_report.print_eachday_report_bonus(dictOfWeather)
                dictOfWeather.clear()
                FILE_READ += 1
        except FileNotFoundError:
            print("File Not Found")
        if FILE_READ == 0:
            print("No data found")
            sys.exit()

else:
    print('Arguments missing')
