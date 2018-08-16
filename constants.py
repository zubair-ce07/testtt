CEND = '\33[0m'
CRED = '\33[31m'
CBLUE = '\33[34m'

COMMANDS = ('-e', '-a', '-c')

USAGE = """\
usage: weatherman.py command argument /path/to/weather/data/files

commands:
-e      For a given year display the highest temperature and day,
        lowest temperature and day, most humid day and humidity.
        Example  Usage: weatherman.py -e 2002 /path/to/files
        Example output:
            Highest: 45C on June 23
            Lowest: 01C on December 22
            Humid: 95% on August 14

-a      For a given month display the average highest temperature,
        average lowest temperature, average humidity.
        Example  Usage: weatherman.py -a 2005/6 /path/to/files
        Example output:
            Highest Average: 39C
            Lowest Average: 18C
            Average Humidity: 71%

-c      For a given month draw one horizontal bar chart on the console
        for the highest and lowest temperature on each day. Highest in
        red and lowest in blue.
        Example  Usage: weatherman.py -c 2011/3 /path/to/files
        Example output:
            March 2011
            01 {0}+++++++++++{1}++++++++++++++++++++++++{2} 11C - 25C
            02 {0}++++++++{1}+++++++++++++++++++++{2} 08C - 22C
""".format(CBLUE, CRED, CEND)