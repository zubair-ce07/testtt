# TASK 1
# Weather Man

# Attached file contains weather data for Lahore from 1996 to 2011. Write an application that generates the following reports.
# You have 4 days to submit the first iteration from the day you are assigned this task.

# 3. For a given month draw two horizontal bar charts on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue.
#
# weatherman.py -c 2011/03 /path/to/files
# March 2011
# 01 ++++++++++++++++++++++++ 25C
# 01 +++++++++++ 11C
# 02 +++++++++++++++++++++ 22C
# 02 ++++++++ 08C

import os.path
import sys

from plainbox.impl import color

# year and path of file arguments
year_arg = sys.argv[1]
pathtofile_arg = sys.argv[2]

#for colorfull output
class color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'


year_arg = str(year_arg).replace("/", '_')
if 1996 <= int(year_arg[:4]) and 2011 >= int(year_arg[:4]):

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    mn = months[int(year_arg[5:]) - 1]
    my_file = os.path.isfile(pathtofile_arg + '/lahore_weather_' + year_arg[:4] + '_' + mn[:3] + '.txt')

    print(mn + ' ' + year_arg[:4])
    if my_file:
        f = open(pathtofile_arg + '/lahore_weather_' + year_arg[:4] + '_' + mn[:3] + '.txt', 'r+')
        count = 1
        for line in f:
            list = line.split(',')
            if list[0].startswith(year_arg[:4]):
                maxTemp = 0 if list[1] == '' else int(list[1])
                print(color.PURPLE +  format(count,'02d')+' ' + color.RED + ('+' * abs(maxTemp))
                      +' '+ color.PURPLE +('0' if list[1] == '' else list[1]) + 'C'
                      )
                minTemp=0 if list[3] == '' else int(list[3])

                print(format(count, '02d') + ' ' + color.BLUE + ('+' * abs(minTemp))
                      + ' ' + color.PURPLE +('0' if list[3] == '' else list[3]) + 'C'
                      )
                count += 1

        f.close()

    else:
        print("invalid file path or file does not exist")

else:
    print('invalid year')
