__author__ = 'mazharshah'


def display_hottest_day_info(info):
    print('\nHottest day of each year:\n')
    headings = ['Year', 'Date', 'Temp']
    print('\t\t\t'.join([str(x) for x in headings]))
    print('--'*19)

    for element in info:
        print('\t\t\t'.join([str(v) for v in element]))


def display_coldest_day_info(info):
    print('\nColdest day of each year:\n')
    headings = ['Year', 'Date', 'Temp']
    print('\t\t\t'.join([str(x) for x in headings]))
    print('--'*19)

    for element in info:
        print('\t\t\t'.join([str(v) for v in element]))


def display_Max_Min_info(info):
    headings = ['Year', 'MAX Temp', 'MIN Temp', 'MAX Humidity', 'Min Humidity']
    print('\t\t'.join([str(x) for x in headings]))
    print '--' * 38
    for element in max_min_Data:
        print('\t\t\t\t'.join([str(x) for x in element]))



import os
list = os.listdir("/home/mazharshah/Desktop/weatherdata/")   # list will have all the names of files within a directory

yearList = range(1996, 2012)
monthList = [
    'Jan', 'Feb', 'Mar',
    'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep',
    'oct', 'Nov', 'Dec'
    ]

max_min_Data = []
hot_day_data = []
cold_day_data = []

path = "/home/mazharshah/Desktop/weatherdata/lahore_weather_"


for year in yearList:

    maxTempList = []
    minTempList = []
    maxHumidityList = []
    minHumidityList = []
    dateMaxTempList = []
    dateMinTempList = []

    for month in monthList:
        file_to_Read = path + str(year) + "_" \
                            + str(month) + ".txt"

        # print file_to_Read
        if file_to_Read[-27:] in list:
            with open(file_to_Read) as f:
                lines = f.readlines()

                for row in lines:
                    line = row.split(',')
                    if len(line) == 23:

                        # Max-Temperature Column# is 1
                        if line[1].isdigit():
                            maxTempList.append(int(line[1]))
                            dateMaxTempList.append(line[0])

                        # Min Temperature Column# is 3
                        if line[3].isdigit():
                            minTempList.append(int(line[3]))
                            dateMinTempList.append(line[0])

                        # Max Humidity Column# is 7
                        if line[7].isdigit():
                            maxHumidityList.append(int(line[7]))

                        # Min Humidity Column# is 9
                        if line[9].isdigit():
                            minHumidityList.append(int(line[9]))

    maxTemperature = max(maxTempList)
    minTemperature = min(minTempList)

    # Making one Row of a result! i.e. for Max-Min Temperature
    yearlyData = [
        year, maxTemperature,
        minTemperature,
        max(maxHumidityList),
        min(minHumidityList)
    ]

    # This is the ROW of Hottest day table
    hot_day_info = [year,
                    dateMaxTempList[maxTempList.index(max(maxTempList))],
                    maxTemperature
    ]

    # This is the Row of Coldest Day table
    cold_day_info = [year,
                     dateMinTempList[minTempList.index(minTemperature)],
                     minTemperature
    ]

    max_min_Data.append(yearlyData)         # Contains every year's Max-Min Temperature
    hot_day_data.append(hot_day_info)       # Contains Every year's Hottest day and Temp
    cold_day_data.append(cold_day_info)     # Contains Every year's Coldest day and Temp


print display_hottest_day_info(hot_day_data)
print display_coldest_day_info(cold_day_data)
print display_Max_Min_info(max_min_Data)

