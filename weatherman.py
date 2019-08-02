import copy
import csv
import sys
import os

dic = {
    "PKT": None,
    "Max TemperatureC": None,
    "Mean TemperatureC": None,
    "Min TemperatureC": None,
    "Dew PointC": None,
    "MeanDew PointC": None,
    "Min DewpointC": None,
    "Max Humidity": None,
    "Mean Humidity": None,
    "Min Humidity": None,
    "Max Sea Level PressurehPa": None,
    "Mean Sea Level PressurehPa": None,
    "Min Sea Level PressurehPa": None,
    "Max VisibilityKm": None,
    "Mean VisibilityKm": None,
    "Min VisibilitykM": None,
    "Max Wind SpeedKm/h": None,
    "Mean Wind SpeedKm/h": None,
    "Max Gust SpeedKm/h": None,
    "Precipitationmm": None,
    "CloudCover": None,
    "Events": None,
    "WindDirDegrees": None
}
day = []
list_month = []
list_year = []
month_check = ["Jan", "Feb",
               "Mar", "Apr",
               "May", "jun",
               "Jul", "Aug",
               "Sep", "Oct",
               "nov", "Dec"]
year_check = [2004, 2005, 2006, 2007, 2008, 2009,
              2010, 2011, 2012, 2013, 2014, 2015, 2016]


def read_year(year):
    list_month.clear()
    list_year.clear()
    for count in range(12):
        day.clear()
        try:
            with open("Murree_weather_"+str(year) + '_' +
                      month_check[count]+".txt", "r") as csvFile:
                reader = csv.reader(csvFile)
                next(reader)
                for data in reader:
                    dic.update([('PKT', data[0]),
                                ('Max TemperatureC', data[1]),
                                ('Mean TemperatureC',
                                 data[2]), ('Min TemperatureC', data[3]),
                                ('Dew PointC',
                                 data[4]), ('MeanDew PointC', data[5]),
                                ('Min DewpointC',
                                 data[6]), ('Max Humidity', data[7]),
                                ('Mean Humidity',
                                 data[8]), ('Min Humidity', data[9]),
                                ('Max Sea Level PressurehPa',
                                 data[10]), ('Mean Sea Level' +
                                'PressurehPa', data[11]),
                                ('Min Sea Level PressurehPa',
                                 data[12]), ('Max VisibilityKm', data[13]),
                                ('Mean VisibilityKm',
                                 data[14]), ('Min VisibilitykM', data[15]),
                                ('Max Wind SpeedKm/h',
                                 data[16]), ('Mean Wind SpeedKm/h', data[17]),
                                ('Max Gust SpeedKm/h',
                                 data[18]), ('Precipitationmm', data[19]),
                                ('CloudCover', data[20]), ('Events', data[21]),
                                ('WindDirDegrees', data[22])])
                    day.append(copy.deepcopy(dic))
            list_month.append(copy.deepcopy(day))
            csvFile.close()
        except IOError:
            list_month.append(None)


def read_months(month):
    list_month.clear()
    list_year.clear()
    for count in range(len(year_check)):
        day.clear()
        try:
            with open("Murree_weather_"+str(year_check[count]) +
                      "_"+month+".txt", "r") as csvFile:
                reader = csv.reader(csvFile)
                next(reader)
                for data in reader:
                    dic.update([('PKT', data[0]), ('Max TemperatureC',
                                data[1]),
                                ('Mean TemperatureC',
                                 data[2]), ('Min TemperatureC', data[3]),
                                ('Dew PointC',
                                 data[4]), ('MeanDew PointC', data[5]),
                                ('Min DewpointC',
                                 data[6]), ('Max Humidity', data[7]),
                                ('Mean Humidity',
                                 data[8]), ('Min Humidity', data[9]),
                                ('Max Sea Level PressurehPa',
                                 data[10]), ('Mean Sea Level PressurehPa',
                                             data[11]),
                                ('Min Sea Level PressurehPa',
                                 data[12]), ('Max VisibilityKm', data[13]),
                                ('Mean VisibilityKm',
                                 data[14]), ('Min VisibilitykM', data[15]),
                                ('Max Wind SpeedKm/h',
                                 data[16]), ('Mean Wind SpeedKm/h', data[17]),
                                ('Max Gust SpeedKm/h',
                                 data[18]), ('Precipitationmm', data[19]),
                                ('CloudCover', data[20]), ('Events', data[21]),
                                ('WindDirDegrees', data[22])])
                    day.append(copy.deepcopy(dic))
            list_year.append(copy.deepcopy(day))
            csvFile.close()
        except IOError:
            list_year.append(None)


def task1():
    year = input("Enter Year 2004 -- 2016 : ")
    read_year(year)
    Max_TemperatureC = -999999
    Max_TemperatureC_Day = None
    Min_TemperatureC = 999999
    Min_TemperatureC_Day = None
    Max_Humidity = -99999
    Max_Humidity_Day = None

    for year in range(12):
        if list_month[year] is not None:
            for data in list_month[year]:
                if data["Max TemperatureC"] != '':
                    if Max_TemperatureC < int(data["Max TemperatureC"]):
                        Max_TemperatureC = int(data["Max TemperatureC"])
                        Max_TemperatureC_Day = data["PKT"]
                if data["Min TemperatureC"] != '':
                    if Min_TemperatureC > int(data["Min TemperatureC"]):
                        Min_TemperatureC = int(data["Min TemperatureC"])
                        Min_TemperatureC_Day = data["PKT"]
                if data["Max Humidity"] != '':
                    if Max_Humidity < int(data["Max Humidity"]):
                        Max_Humidity = int(data["Max Humidity"])
                        Max_Humidity_Day = data["PKT"]

    print(Max_TemperatureC, "C ", Max_TemperatureC_Day)
    print(Min_TemperatureC, "C ", Min_TemperatureC_Day)
    print(Max_Humidity, "% ", Max_Humidity_Day)


def task2():
    month_index = None
    Mon = input("Enter month first three alphbets:")
    Mon = Mon.capitalize()
    for month in month_check:
        if Mon == month:
            month_index = month_check.index(month)
            break
    read_months(month_check[month_index])

    average_highest_temperature = None
    highest_temperature = 0
    highest_temperature_count = 0

    average_lowest_temperature = None
    lowest_temperature = 0
    lowest_temperature_count = 0

    average_mean_humidity = None
    mean_humidity = 0
    mean_humidity_count = 0

    for count in range(len(list_year)):
        if list_year[count] is not None:
            for data in list_year[count]:
                if data["Max TemperatureC"] != '':
                    highest_temperature += int(data["Max TemperatureC"])
                    highest_temperature_count += 1
                if data["Min TemperatureC"] != '':
                    lowest_temperature = int(data["Min TemperatureC"])
                    lowest_temperature_count += 1
                if data["Mean Humidity"] != '':
                    mean_humidity = int(data["Mean Humidity"])
                    mean_humidity_count += 1

    average_highest_temperature = highest_temperature/highest_temperature_count
    average_lowest_temperature = lowest_temperature/lowest_temperature_count
    average_mean_humidity = mean_humidity/mean_humidity_count

    print("Average highest temperature in " + Mon +
          " is: ", average_highest_temperature)
    print("Average lowest temperature in " + Mon +
          " is: ", average_lowest_temperature)
    print("Average mean humidity in " + Mon + " is: ", average_mean_humidity)


def read_one_month(month, year):
    list_month.clear()
    list_year.clear()
    day.clear()
    try:
        with open("Murree_weather_"+year+"_"+month+".txt", "r") as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            for data in reader:
                dic.update([('PKT', data[0]), ('Max TemperatureC', data[1]),
                            ('Mean TemperatureC',
                             data[2]), ('Min TemperatureC', data[3]),
                            ('Dew PointC', data[4]
                             ), ('MeanDew PointC', data[5]),
                            ('Min DewpointC', data[6]
                             ), ('Max Humidity', data[7]),
                            ('Mean Humidity', data[8]
                             ), ('Min Humidity', data[9]),
                            ('Max Sea Level PressurehPa',
                            data[10]), ('Mean Sea Level PressurehPa',
                                        data[11]),
                            ('Min Sea Level PressurehPa',
                             data[12]), ('Max VisibilityKm', data[13]),
                            ('Mean VisibilityKm',
                             data[14]), ('Min VisibilitykM', data[15]),
                            ('Max Wind SpeedKm/h',
                             data[16]), ('Mean Wind SpeedKm/h', data[17]),
                            ('Max Gust SpeedKm/h',
                             data[18]), ('Precipitationmm', data[19]),
                            ('CloudCover', data[20]), ('Events', data[21]),
                            ('WindDirDegrees', data[22])])
                day.append(copy.deepcopy(dic))
        csvFile.close()
    except IOError:
        list_year.append(None)


def task3():
    month = input("Enter month ( First three alphabets ) :")
    year = input("Enter year (2004 to 2016) : ")
    read_one_month(month.capitalize(), str(year))
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    RESET = "\033[0;0m"
    if day is not None:
        for data in day:
            print(data["PKT"], end='')
            # max temp
            max_temp = data["Max TemperatureC"]
            sys.stdout.write(RED)
            if max_temp != "":
                for count in range(int(max_temp)):
                    print("+", end="")
                sys.stdout.write(RESET)
                print(" ", max_temp, "C")
            sys.stdout.write(RESET)
            # min temp
            print(data["PKT"], end='')
            min_tmep = data["Min TemperatureC"]
            sys.stdout.write(BLUE)
            if min_tmep != "":
                for count in range(int(min_tmep)):
                    print("+", end="")
                sys.stdout.write(RESET)
                print(" ", min_tmep, "C")
            sys.stdout.write(RESET)

    else:
        print("NO data found")


def task4():
    print("\nTask1 : ")
    task1()
    print("\nTask2 : ")
    task2()
    print("\nTask3 : ")
    task3()


def task5():
    month = input("Enter month ( First three alphabets ) :")
    year = input("Enter year (2004 to 2016) : ")
    read_one_month(month.capitalize(), str(year))
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    RESET = "\033[0;0m"
    if day is not None:
        for data in day:
            print(data["PKT"], end='')
            # min temp
            min_tmep = data["Min TemperatureC"]
            sys.stdout.write(BLUE)
            if min_tmep != "":
                for count in range(int(min_tmep)):
                    print("+", end="")
            # max temp
            max_temp = data["Max TemperatureC"]
            sys.stdout.write(RED)
            if max_temp != "":
                for count in range(int(max_temp)):
                    print("+", end="")
                sys.stdout.write(RESET)
                print(" ", min_tmep, "C", end=" ")
                print(" ", max_temp, "C")
            sys.stdout.write(RESET)

    else:
        print("NO data found")


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    task1()

    task2()

    task3()

    task4()

    task5()
