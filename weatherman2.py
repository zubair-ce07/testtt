# TASK 1
# Weather Man

# Attached file contains weather data for Lahore from 1996 to 2011. Write an application that generates the following reports.
# You have 4 days to submit the first iteration from the day you are assigned this task.

# 2. For a given month display the average highest temperature, average lowest temperature, average humidity.

# weatherman.py -a 2005/6 /path/to/files
# Highest Average: 39C
# Lowest Average: 18C
# Average Humidity: 71%

import os.path
import sys

# year and path of file arguments
year_arg = sys.argv[1]
pathtofile_arg = sys.argv[2]
year_arg = str(year_arg).replace("/", '_')
if 1996 <= int(year_arg[:4]) and 2011 >= int(year_arg[:4]):

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    mn = months[int(year_arg[5:]) - 1]
    my_file = os.path.isfile(pathtofile_arg + '/lahore_weather_' + year_arg[:4] + '_' + mn[:3] + '.txt')

    count = 0
    ltcount = 0
    htcount = 0
    ltsum = 0
    htsum = 0
    hcount = 0
    hsum = 0

    if my_file:
        f = open(pathtofile_arg + '/lahore_weather_' + year_arg[:4] + '_' + mn[:3] + '.txt', 'r+')

        for line in f:
            list = line.split(',')
            if list[0].startswith(year_arg[:4]):
                if list[1] != '':
                    htcount = htcount + 1
                    htsum = htsum + int(list[1])

                if list[3] != '':
                    ltcount = ltcount + 1
                    ltsum = ltsum + int(list[3])

                if list[8] != '':
                    hcount = hcount + 1
                    hsum = hsum + int(list[8])

        f.close()
    else:
        print("invalid file path or file does not exist")

    if htcount != 0:
        print("Highest Average: " +str( round(htsum/htcount, 2))+"C")
    else:
        print("Highest Average Not Found")

    if ltcount != 0:
        print("Lowest Average: " + str(round(ltsum / ltcount, 2))+"C")
    else:
        print("Lowest Average Not Found")

    if hcount != 0:
        print("Average Mean Humidity: " + str(round(hsum / hcount, 2))+"%")
    else:
        print("Humidity Not Found")

else:
    print('invalid year')
