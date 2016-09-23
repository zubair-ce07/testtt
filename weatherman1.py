# TASK 1
# Weather Man

# Attached file contains weather data for Lahore from 1996 to 2011. Write an application that generates the following reports.
# You have 4 days to submit the first iteration from the day you are assigned this task.

# 1. For a given year display the highest temperature and day, lowest temperature and day, most humid day and humidity.

# weatherman.py -e 2002 /path/to/files
#  Highest: 45C on June 23
#  Lowest: 01C on December 22
#  Humid: 95% on August 14

import os.path
import sys

# year and path of file arguments
year_arg = sys.argv[1]
pathtofile_arg = sys.argv[2]

if 1996 <= int(year_arg) and 2011 >= int(year_arg):
    count = 0
    HighestTemp = 0
    LowestTemp = 1000
    HighestTempDay = 'none'
    LowestTempDay = 'none'
    MostHumidDay = 'none'
    MHumidity = 0

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    for m in months:
        my_file = os.path.isfile(pathtofile_arg + '/lahore_weather_' + year_arg + '_' + m[:3] + '.txt')
        if my_file:
            f = open(pathtofile_arg + '/lahore_weather_' + year_arg + '_' + m[:3] + '.txt', 'r+')

            for line in f:

                list = line.split(',')
                if len(list) > 5 and list[0].startswith(year_arg):

                    list[1] = int(list[1]) if list[1].strip() else 0
                    list[3] = int(list[3]) if list[3].strip() else 1000
                    list[7] = int(list[7]) if list[7].strip() else 0

                    if list[1] > HighestTemp:
                        HighestTemp = list[1]
                        HighestTempDay = list[0]
                    if list[3] < LowestTemp and list[3] != 1000:
                        LowestTemp = list[3]
                        LowestTempDay = list[0]
                    if list[7] > MHumidity:
                        MHumidity = list[7]
                        MostHumidDay = list[0]

            f.close()
        else:
            count = count + 1
            if count >= 12:
                print("invalid file path or file does not exist")

    if HighestTemp != 0:
        yr, mn, dt = HighestTempDay.split('-')
        print("Highest: " + format(HighestTemp, '02d') + "C on " + months[int(mn) - 1] + " " + dt)
    else:
        print("Highest Temp Not Found")
    if LowestTemp != 1000:
        yr, mn, dt = LowestTempDay.split('-')
        print("Lowest: " + format(LowestTemp, '02d') + "C on " + months[int(mn) - 1] + " " + dt)
    else:
        print("Lowest Temp Not Found")
    if MHumidity != 0:
        yr, mn, dt = MostHumidDay.split('-')
        print("Humid: " + format(MHumidity, '02d') + "% on " + months[int(mn) - 1] + " " + dt)
    else:
        print("Highest Humidity Not Found")
else:
    print('invalid year')
